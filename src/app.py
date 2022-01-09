import json
import logging
import os
import pathlib
import shutil
import sys
import socket
import requests
from installed_softwares import InstalledSoftware
from invertedIndex import InvertedIndex, save_pickle, load_pickle
from searchEngine import SearchEngineBuilder, CpeSwFitter
from xmlParser import CpeXmlParser
import download_db
import datetime


class App:
    def __init__(self, bool_update_cve=False, bool_update_cpe=False, bool_update_local_sw=False, threshold=0.6):
        self.update_cve = bool_update_cve
        self.update_cpe = bool_update_cpe
        self.update_local_sw = bool_update_local_sw
        self.update_my_cpe = self.update_cpe or self.update_local_sw
        self.update_my_cve = self.update_my_cpe or self.update_cve
        self.threshold = threshold
        pathlib.Path('./resources').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./models').mkdir(parents=True, exist_ok=True)
        pathlib.Path('./logs').mkdir(parents=True, exist_ok=True)
        log_name = fr'./logs/scan_{datetime.datetime.now().strftime("%d_%m-%H_%M_%S")}.log'
        logging.basicConfig(filename=log_name,
                            filemode='a',
                            format='%(asctime)s %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger('NvdScannerRezilion')

    def scan(self, cpe_s, inverted_ind):
        self.logger.info("scanning...")
        cve_dict = {}
        for cpe in cpe_s.values.tolist():
            if cpe in inverted_ind.inverted_index:
                cve_dict[cpe] = inverted_ind.inverted_index[cpe]
        json.dump(cve_dict, open("./resources/My_cves.json", 'w'))
        self.logger.info("For your results look for My_cves.json at /resources")
        return cve_dict

    def download_cpe_xml(self):
        """
            Download CPE dictionary
            """
        if self.update_cpe or not os.path.exists('./resources/official-cpe-dictionary_v2.3.xml'):
            self.logger.info("Download CPE dictionary")
            download_db.download_cpe_dict()
            self.logger.info("CPE dict downloaded")
            download_db.unzip_file('./resources/official-cpe-dictionary_v2.3.xml.zip', './resources/')
            self.logger.info("CPE dict unzipped")

    def parse_cpe_xml(self):
        """
            Parse CPE dict xml to a csv
            """
        if self.update_cpe or not os.path.exists("./resources/parsed_xml.csv"):
            self.logger.info("Parse CPE dict xml to a csv")
            parser = CpeXmlParser('./resources/official-cpe-dictionary_v2.3.xml')
            parser.csv_creator('./resources/official-cpe-dictionary_v2.3.xml')
            self.logger.info("CPE dict xml parsed")

    def get_local_sw(self):
        """
            Get local software's
            """
        if self.update_local_sw or not os.path.exists("./resources/registry_data.json"):
            self.logger.info("Get local software's from Registry")
            i_s = InstalledSoftware()
            i_s.dump_software_lst_to_json(["Publisher", 'DisplayVersion', 'DisplayName'])
            self.logger.info("Local softwares info Extracted")

    def build_searcher(self):
        """
            Build searcher for scanning
            """
        tmp_bool = not os.path.exists('./models/dictionary.gensim') \
                   or not os.path.exists('./models/corpus_tfidf.pkl') \
                   or not os.path.exists('./models/similarity_matrix.gensim')
        if tmp_bool or self.update_cpe:
            self.logger.info("Build searcher for scanning")
            search_builder = SearchEngineBuilder()
            search_builder.create_models("./resources/parsed_xml.csv")
            self.logger.info("Models created. (gensim dict, tfidf corpus and similarity matrix)")

    def find_my_cpe(self):
        self.logger.info("Fit my software's to cpe's")
        cpe_sw_fitter = CpeSwFitter("./resources/parsed_xml.csv", self.update_my_cpe)
        self.logger.info("Models loaded.")
        my_cpe_ = cpe_sw_fitter.fit_all(1, self.threshold)
        self.logger.info(f"CPEs fitted to local softwares list by searcher. threshold: {self.threshold}")
        return my_cpe_

    def download_cve_dicts(self):
        """
        Download CVE dicts
        """
        cve_year_dict_ = ''
        if self.update_cve or not os.path.exists("./models/inverted_index.pkl"):
            ddb = download_db.DownloadDb()
            cve_year_dict_ = ddb.cve_dict
        return cve_year_dict_

    def build_inverted_ind(self, cve_year_dict_):
        invInd_ = InvertedIndex()
        """
            Build inverted index of cpes to cves
        """
        if self.update_cve or not os.path.exists("./models/inverted_index.pkl"):
            invInd_.extract_data_all_dir(cve_year_dict_)
        else:
            invInd_.inverted_index = load_pickle("./models/inverted_index")
            self.logger.info("Inverted index loaded")
        return invInd_


