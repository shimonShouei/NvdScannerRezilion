import json
import logging
import os
import pathlib
import sys
import traceback
from io import StringIO

import pandas as pd

from installed_softwares import InstalledSoftware
from invertedIndex import InvertedIndex, save_pickle, load_pickle
from searchEngine import SearchEngineBuilder, CpeSwFitter
from xmlParser import CpeXmlParser
import download_db
import datetime


def scan(cpe_s, inverted_ind):
    cve_dict = {}
    for cpe in cpe_s.values.tolist():
        if cpe in inverted_ind.inverted_index:
            cve_dict[cpe] = inverted_ind.inverted_index[cpe]

    json.dump(cve_dict, open("./resources/My_cves.json", 'w'))


if __name__ == '__main__':
    args = sys.argv
    bool_update_resources = False
    bool_update_models = False
    threshold = 0.6
    if len(args) == 4:
        bool_update_resources = int(args[1])
        bool_update_models = int(args[2])
        threshold = int(args[3])
    pathlib.Path('./resources').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./resources/cve').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./models').mkdir(parents=True, exist_ok=True)
    pathlib.Path('./logs').mkdir(parents=True, exist_ok=True)
    log_name = fr'./logs/scan_{datetime.datetime.now().strftime("%d_%m-%H_%M_%S")}.log'
    logger = logging.getLogger('NvdScannerRezilion')
    logging.basicConfig(filename=log_name,
                        filemode='a',
                        format='%(asctime)s %(message)s',
                        level=logging.INFO)
    try:
        """
        Download CPE dictionary
        """
        if not os.path.exists('./resources/official-cpe-dictionary_v2.3.xml'):
            logger.info("Download CPE dictionary")
            download_db.download_cpe_dict()
            logger.info("CPE dict downloaded")
            download_db.unzip_file('./resources/official-cpe-dictionary_v2.3.xml.zip', './resources/')
            logger.info("CPE dict unzipped")
        """
        Parse CPE dict xml to a csv
        """
        if not os.path.exists("./resources/parsed_xml.csv"):
            logger.info("Parse CPE dict xml to a csv")
            a = CpeXmlParser('./resources/official-cpe-dictionary_v2.3.xml')
            a.csv_creator('./resources/official-cpe-dictionary_v2.3.xml')
            logger.info("CPE dict xml parsed")

        """
        Get local software's
        """
        if not os.path.exists("./resources/registry_data.json"):
            logger.info("Get local software's from Registry")
            i_s = InstalledSoftware()
            i_s.dump_software_lst_to_json(["Publisher", 'DisplayVersion', 'DisplayName'])
            logger.info("Local softwares info Extracted")
        """
        Build and use searcher for scanning
        """
        tmp_bool = not os.path.exists('./models/dictionary.gensim') \
                   or not os.path.exists('./models/corpus_tfidf.pkl') \
                   or not os.path.exists('./models/similarity_matrix.gensim')
        if tmp_bool or bool_update_models:
            logger.info("Build searcher for scanning")
            search_builder = SearchEngineBuilder()
            search_builder.create_models("./resources/parsed_xml.csv")
            logger.info("Models created. (gensim dict, tfidf corpus and similarity matrix")
        logger.info("Fit my software's to cpe's")
        cpe_sw_fitter = CpeSwFitter("./resources/parsed_xml.csv", bool_update_models)
        logger.info("Models loaded.")
        threshold = 0.6
        my_cpe = cpe_sw_fitter.fit_all(1, threshold)
        logger.info(f"CPEs fitted to local softwares list by searcher. threshold: {threshold}")
        """
        Download CVE dicts
        """
        ddb = download_db.DownloadDb()
        """
        Build inverted index of cpes to cves
        """
        invInd = InvertedIndex()
        invInd.extract_data_all_dir(ddb.cve_dict)
        logger.info("scanning...")
        scan(my_cpe, invInd)
        logger.info("End")
        logger.info("For your results look for My_cves.json at /resources")
    except Exception as e:
        logger.error(e, exc_info=True)
