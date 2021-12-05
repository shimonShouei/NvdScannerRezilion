import pickle
import pandas as pd
import numpy as np
import pathlib
from gensim import corpora
from gensim.models import TfidfModel
from gensim import similarities
from tqdm import tqdm

stop_word = ['corporation']


def parse_doc(doc):
    parsed_doc = doc.split(" ")
    if doc.__contains__("One"):
        print('d')
    parsed_doc = list(set([x.lower() for x in parsed_doc if x.lower() not in stop_word]))
    return parsed_doc


def load_pickle(file_path):
    infile = open(file_path, 'rb')
    file = pickle.load(infile)
    infile.close()
    return file


class CpeSwFitter:
    def __init__(self, parsed_xml_path, sim_func_name):
        self.registry_data = pd.read_json("registry_data.json")
        self.dictionary = load_pickle('./models/dictionary.gensim')
        self.bow_corpus_tfidf = load_pickle('./models/corpus_tfidf.pkl')
        self.similarity_matrix = similarities.SparseMatrixSimilarity.load('./models/similarity_matrix.gensim')
        self.sim_func_name = sim_func_name
        # if sim_func_name == 'cosin':
        #     self.similarity_func = similarities.SoftCosineSimilarity.load('./models/similarity_func_{}.gensim'.format(sim_func_name))
        # elif sim_func_name == 'default':
        #     self.similarity_matrix = similarities.SparseMatrixSimilarity.load('./models/similarity_matrix.gensim')
        self.parsed_xml = pd.read_csv(parsed_xml_path)

    def calc_similarity(self, qry):
        parsed_query = parse_doc(qry)
        if qry.__contains__("One"):
            print('d')
        bow_query = self.similarity_matrix[self.dictionary.doc2bow(parsed_query)]
        res_sim_sorted = np.argsort(bow_query)
        res_sim_sorted_arg = np.sort(bow_query)
        B = np.reshape(np.concatenate([res_sim_sorted, res_sim_sorted_arg]), (2, len(res_sim_sorted))).T
        np_df = pd.DataFrame(B)
        np_df = np_df[np_df[1] > 0]
        return np_df.sort_values(by=[1], ascending=False)

    def searcher(self, qry, num_to_retrieve):
        if qry.__contains__("One"):
            print('d')
        indices_and_score = self.calc_similarity(qry).head(num_to_retrieve)
        relevant_docs = self.parsed_xml.iloc[indices_and_score[0]][["cpe_items", "titles"]].reset_index(drop=True)
        relevant_docs["sim_score"] = indices_and_score[1].iloc[:num_to_retrieve].reset_index(drop=True)
        return relevant_docs

    def fit_all(self, num_to_retrieve):
        final_res = []
        for col in tqdm(self.registry_data):
            query = self.registry_data[col].str.cat(sep=' ', na_rep='')
            relevant_docs = self.searcher(query, num_to_retrieve)
            if relevant_docs.empty:
                final_res.append([query, None, None, 0])
            else:
                final_res.append([query, relevant_docs["cpe_items"].iloc[0], relevant_docs["titles"].iloc[0],
                                  relevant_docs["sim_score"].iloc[0]])
        final_res = pd.DataFrame(final_res)
        final_res.columns = ["registry_sw", "cpe_items", "titles", "sim_score"]
        final_res.to_csv('retrieved_{}.csv'.format(self.sim_func_name))
        print(final_res)
        print("end")


class SearchEngineBuilder:
    def pre_processing(self, parsed_xml_path):
        parsed_xml = pd.read_csv(parsed_xml_path)
        parsed_title_df = parsed_xml["titles"].str.split(' ', n=12, expand=True)
        parsed_df = parsed_title_df
        parsed_df[["vendor", "product", "version"]] = parsed_xml[["vendor", "product", "version"]]
        parsed_df = parsed_df.apply(lambda x: x.str.lower())
        parsed_df["tokens"] = parsed_df.values.tolist()
        parsed_df["tokens"] = parsed_df["tokens"].apply(lambda x: [y for y in x if y is not None and y is not np.nan])
        return parsed_df["tokens"]

    def create_models(self, parsed_xml_path, sim_func_name):
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


if __name__ == "__main__":
    sim_func_names_list = ["cosin"]
    for func in sim_func_names_list:
        # search_builder = SearchEngineBuilder()
        # search_builder.create_models("parsed_xml.csv", func)
        cpe_sw_fitter = CpeSwFitter("parsed_xml.csv", func)
        cpe_sw_fitter.fit_all(1)
