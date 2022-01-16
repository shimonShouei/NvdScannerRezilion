import logging
import os
import pickle
from collections import deque

import numpy
import pandas as pd
import numpy as np
import pathlib
from gensim import corpora
from gensim.models import TfidfModel
from gensim import similarities
from tqdm import tqdm
import re
import itertools


def extract_alpha(token: str, res_list: []):
    new_token = ""
    for char in token:
        if char.isalpha():
            new_token += char
    if len(new_token) > 0:
        res_list.append(new_token)


def stop_words():
    return ['corporation', 'software', 'foundation', 'for']


def parse_version_for_registery(token):
    new_res = ""
    for char in token:
        if char.isnumeric():
            new_res += char
        if char == ".":
            new_res += char
    return new_res


def parse_barkets(token):
    new_res = ""
    for c in token:
        if c != "(" or c != ")":
            new_res += c
    return new_res


def parse_doc(doc: str):
    parsed_doc = str(doc).split()
    parsed_doc = list(set([x.lower() for x in parsed_doc if x.lower() not in stop_words()]))
    result_tokens = []
    for token in parsed_doc:
        # if token.__contains__("_"):
        #     token = token.replace("_", " ")
        if token.isalnum():
            if token.isascii():
                result_tokens.append(token)
        elif any(map(str.isalpha,
                     token)):  # Test if the token contains alpha characters and if so, add only the relevant characters
            extract_alpha(token, result_tokens)
        elif "." in token:
            result_tokens.append(parse_version_for_registery(token))
        elif "(" in token:
            result_tokens.append(parse_barkets(token))

    # print("parsed_doc:  ", parsed_doc)
    # print("result_tokens:  ", result_tokens)
    return list(set(result_tokens))


def load_pickle(file_path):
    infile = open(file_path, 'rb')
    file = pickle.load(infile)
    infile.close()
    return file


class CpeSwFitter:
    def __init__(self, parsed_xml_path, bool_rebuild):
        self.b_rebuild = bool_rebuild
        if self.b_rebuild or not os.path.exists("./resources/My_cpes.csv"):
            self.registry_data = pd.read_json("./resources/registry_data.json")
            self.dictionary = load_pickle('./models/dictionary.gensim')
            self.bow_corpus_tfidf = load_pickle('./models/corpus_tfidf.pkl')
            self.similarity_matrix = similarities.SparseMatrixSimilarity.load('./models/similarity_matrix.gensim')
            # if sim_func_name == 'cosin': self.similarity_func = similarities.SoftCosineSimilarity.load(
            # './models/similarity_func_{}.gensim'.format(sim_func_name)) elif sim_func_name == 'default':
            # self.similarity_matrix = similarities.SparseMatrixSimilarity.load('./models/similarity_matrix.gensim')
            self.parsed_xml = pd.read_csv(parsed_xml_path)

    def calc_similarity(self, qry):
        parsed_query = parse_doc(qry)
        bow_query = self.similarity_matrix[self.dictionary.doc2bow(parsed_query)]
        res_sim_sorted = np.argsort(bow_query)
        res_sim_sorted_arg = np.sort(bow_query)
        B = np.reshape(np.concatenate([res_sim_sorted, res_sim_sorted_arg]), (2, len(res_sim_sorted))).T
        np_df = pd.DataFrame(B)
        # np_df = np_df[np_df[1] > 0]
        return np_df.sort_values(by=[1], ascending=False)

    def searcher(self, qry, num_to_retrieve):
        indices_and_score = self.calc_similarity(qry).head(num_to_retrieve)
        relevant_docs = self.parsed_xml.iloc[indices_and_score[0]][["cpe_23_names", "titles"]].reset_index(drop=True)
        relevant_docs["sim_score"] = indices_and_score[1].iloc[:num_to_retrieve].reset_index(drop=True)
        return relevant_docs

    def fit_all(self, num_to_retrieve, thresh):
        logger = logging.getLogger('NvdScannerRezilion')
        if self.b_rebuild or not os.path.exists("./resources/My_cpes.csv"):
            final_res = []
            for col in tqdm(self.registry_data):
                query = self.registry_data[col].str.cat(sep=' ', na_rep='')
                relevant_docs = self.searcher(query, num_to_retrieve)
                for i in range(len(relevant_docs)):
                    if relevant_docs.empty:
                        final_res.append([query, None, None, 0])
                    else:
                        final_res.append([query, relevant_docs["cpe_23_names"].iloc[i], relevant_docs["titles"].iloc[i],
                                          relevant_docs["sim_score"].iloc[i]])
            final_res = pd.DataFrame(final_res)
            final_res.columns = ["registry_sw", "cpe_23_names", "titles", "sim_score"]
            final_res.to_csv('./resources/My_cpes.csv')
            # print(final_res)
            logger.info("My cpe's created")
            print("My cpe's created")
        else:
            final_res = pd.read_csv('./resources/My_cpes.csv')
            logger.info("My cpe's loaded")
            print("My cpe's loaded")
        return final_res.loc[final_res["sim_score"] >= thresh]["cpe_23_names"]


class SearchEngineBuilder:

    @staticmethod
    def parse_title(param):
        if param is not None:
            new_string = ""
            for s in param:
                if s.isalpha():
                    new_string += s
            return new_string

    @staticmethod
    def parse_version(str: str):
        new_string = re.sub(r'[a-zA-Z]', '', str)
        new_string = new_string.replace("\\", "")
        return new_string

    def pre_processing(self, parsed_xml_path):
        parsed_xml = pd.read_csv(parsed_xml_path)
        parsed_title_df = parsed_xml["titles"].str.split(' ', n=12, expand=True)

        # parsed_title_df = parsed_title_df.apply(lambda x: [y for y in x if y is not None and y is not np.nan])
        for column in parsed_title_df:
            parsed_title_df[column] = parsed_title_df[column].apply(lambda x: self.parse_title(str(x)))

        # for rowIndex, row in parsed_title_df.iterrows():  # iterate over rows
        #     for columnIndex, value in row.items():
        #         if row[columnIndex] is not None and row[columnIndex] is not np.nan:
        #             row[columnIndex] = parse_title(row[columnIndex])
        parsed_df = parsed_title_df
        parsed_df[["vendor", "product", "version"]] = parsed_xml[["vendor", "product", "version"]]
        parsed_df = parsed_df.apply(lambda x: x.str.lower())
        parsed_df["version"] = parsed_df["version"].apply(lambda x: self.parse_version(str(x)))
        parsed_df["tokens"] = parsed_df.values.tolist()
        parsed_df["tokens"] = parsed_df["tokens"].apply(lambda x: [y for y in x if y is not None and y is not np.nan])
        # parsed_df.to_csv('parse_df{}.csv')
        return parsed_df["tokens"]

    def get_tokens(self, list_to_add: [], res_list: []):
        for token in list_to_add:
            res_list.extend(token)

    def create_models(self, parsed_xml_path):
        tokenized_data = self.pre_processing(parsed_xml_path)
        dictionary = corpora.Dictionary(tokenized_data)
        bow_corpus = [dictionary.doc2bow(text) for text in tqdm(tokenized_data)]
        tfidf = TfidfModel(bow_corpus)
        bow_corpus_tfidf = tfidf[bow_corpus]
        similarity_matrix = similarities.SparseMatrixSimilarity(bow_corpus_tfidf, num_features=len(dictionary))

        # if sim_func_name == 'cosin':
        #     cossin_sim_model = similarities.SoftCosineSimilarity(bow_corpus_tfidf, similarity_matrix)
        #     cossin_sim_model.save('./models/similarity_func_{}.gensim'.format(sim_func_name))
        # elif sim_func_name == 'default':
        #     similarity_matrix = similarities.SparseMatrixSimilarity(bow_corpus_tfidf, num_features=len(dictionary))
        pathlib.Path("./models").mkdir(parents=True, exist_ok=True)
        dictionary.save('./models/dictionary.gensim')
        pickle.dump(bow_corpus_tfidf, open('./models/corpus_tfidf.pkl', 'wb'))
        similarity_matrix.save('./models/similarity_matrix.gensim')
