import logging
import os

import requests
import re
from os import listdir
from os.path import isfile, join
import zipfile
import json
import pathlib
import wget
from tqdm import tqdm

logger = logging.getLogger('NvdScannerRezilion')

class DownloadDb:
    cve_dict = {}

    def __init__(self):
        if 'cve' not in listdir("resources"):
            logger.info("Download CVE dicts")
            pathlib.Path('./resources/cve').mkdir(parents=True, exist_ok=True)
            self.download_all_zips_files()
            logger.info("All CVEs data downloaded from NVD website.")
        logger.info("Load CVE dicts")
        files = [f for f in listdir("./resources/cve/") if isfile(join("./resources/cve/", f))]
        files.sort()
        for file_name in tqdm(files):
            year = file_name[11:15]
            archive = zipfile.ZipFile(join("./resources/cve/", file_name), 'r')
            jsonfile = archive.open(archive.namelist()[0])
            self.cve_dict[year] = json.loads(jsonfile.read())
            jsonfile.close()
            logger.info(f"{year} CVEs file loaded.")
        logger.info("All CVEs data loaded.")


    @staticmethod
    def download_all_zips_files():
        """
       This function, perform get requests from the NVD site for all vulnerabilities data files which finish with ".json.zip"
       Finally the function writes all the files to NVD folder on the local disk
        :return:
        """
        r = requests.get('https://nvd.nist.gov/vuln/data-feeds#JSON_FEED')
        for filename in tqdm(re.findall("nvdcve-1.1-[0-9]*\.json\.zip", r.text)):
            r_file = requests.get("https://nvd.nist.gov/feeds/json/cve/1.1/" + filename, stream=True)
            with open("./resources/cve/" + filename, 'wb') as f:
                logger.info(f"Download {filename}")
                for chunk in r_file:
                    f.write(chunk)


def download_cpe_dict():
    url = 'https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip'
    # wget.download(url)
    r_file = requests.get(url, stream=True)
    abs_path = os.path.abspath("./resources/official-cpe-dictionary_v2.3.xml.zip")
    with open(abs_path, 'wb') as f:
        for chunk in tqdm(r_file):
            f.write(chunk)


def unzip_file(file_name, directory_to_extract=None):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract)
    os.remove(file_name)  # removing the .zip file


