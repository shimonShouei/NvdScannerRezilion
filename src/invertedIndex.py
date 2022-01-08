import logging
import os
import pickle
from tqdm import tqdm
import json

logger = logging.getLogger('NvdScannerRezilion')

def load_pickle(file_path):
    infile = open(file_path+".pkl", 'rb')
    file = pickle.load(infile)
    infile.close()
    return file


def save_pickle(obj, file_name):
    with open(file_name + ".pkl", "wb") as f:
        pickle.dump(obj, f)
    # pickle.dump(obj, file_name+".pkl")


class InvertedIndex:

    def __init__(self):
        self.inverted_index = {}

    def extract_data_one_file(self, cve_d):
        # with open("cve\\{}".format(file_name), encoding="utf8") as f:
        #     cves = json.load(f)
        for cve in cve_d["CVE_Items"]:
            nodes = cve["configurations"]["nodes"]
            for node in nodes:
                for cpe in node["cpe_match"]:
                    cpe_key = cpe["cpe23Uri"]
                    cve_id = cve["cve"]["CVE_data_meta"]["ID"]
                    cve_det = {
                               "DESC": cve["cve"]["description"]["description_data"][0]["value"],
                               }
                    try:
                        cve_det["SEVERITY"] = cve["impact"]["baseMetricV3"]["cvss3"]["baseSeverity"]
                    except KeyError:
                        cve_det["SEVERITY"] = cve["impact"]["baseMetricV2"]["severity"]
                    try:
                        cve_det["ASSIGNER"] = cve["cve"]["CVE_data_meta"]["ASSIGNER"],
                    except KeyError:
                        cve_det["SEVERITY"] = ''

                    if cpe_key in self.inverted_index:
                        self.inverted_index[cpe_key][cve_id] = cve_det
                    else:
                        self.inverted_index[cpe_key] = {cve_id: cve_det}

    # for root, dirs, files in os.walk("cve"):
    #     for file in files:
    #         if re.compile('(.*zip$)').match(file):
    #             dd.unzip_file("{}\{}".format(root, file), root)

    def extract_data_all_dir(self, cve_dict_by_Name):
        if not os.path.exists("./models/inverted_index.pkl"):
            for cve_dict in tqdm(cve_dict_by_Name.values()):
                self.extract_data_one_file(cve_dict)
            save_pickle(self.inverted_index, "./models/inverted_index")
            logger.info("Inverted index created")
        else:
            self.inverted_index = load_pickle("./models/inverted_index")
            logger.info("Inverted index loaded")
