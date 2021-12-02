import xml.etree.ElementTree as et
from utils import *
from difflib import SequenceMatcher

import pandas as pd
from installed_softwares import InstalledSoftware

cpe_xml_file_name = 'official-cpe-dictionary_v2.3.xml'
parsed_cpe_csv_file_name = 'parsed_xml.csv'
reg_data_file_name = 'registry_data.json'


class CpePdDataAccess:
    def __init__(self, cpe_dict_file_name, reg_list_file_name):
        self.cpe_data = pd.read_csv(cpe_dict_file_name)
        self.installed_software_getter = InstalledSoftware()
        self.registry_data = pd.read_json(reg_list_file_name)

    def find_cpe_by_software(self, publisher, display_version, display_name):
        publisher_split = publisher.split(' ')
        display_version_split = display_version.split('.')
        temp1 = self.cpe_data[self.cpe_data.vendor.str.contains(' '.join(publisher_split[:2]).lower() + '|' + publisher_split[0].lower())]
        res = []
        for i, row in temp1.iterrows():
            ratio = SequenceMatcher(display_version, row['titles']).ratio()
            if ratio > 0:
                res.append((row['titles'], ))
        # temp2 = temp1[temp1.version.str.contains('|'.join([' '.join(display_version_split[:i]).lower() for i in range(len(display_version_split))]))]
        res = sorted(res, key=lambda x: x[1])
        return res
        # temp = temp[temp.version.str.contains]


class CpeXmlParser:
    def __init__(self, file_name):
        self.tree = et.parse(file_name)
        self.root = self.tree.getroot()

        self.namespaces = {'': 'http://cpe.mitre.org/dictionary/2.0',
                           'xsi': "http://www.w3.org/2001/XMLSchema-instance",
                           'scap-core': "http://scap.nist.gov/schema/scap-core/0.3",
                           'cpe-23': "http://scap.nist.gov/schema/cpe-extension/2.3",
                           "ns6": "http://scap.nist.gov/schema/scap-core/0.1",
                           'meta': "http://scap.nist.gov/schema/cpe-dictionary-metadata/0.2"}

    def get_all_cpe_items(self):
        return self.root.findall('cpe-item', self.namespaces)

    def get_all_cpe_items_names(self):
        cpe_names = []
        for cpe_item in self.get_all_cpe_items():
            cpe_names.append(cpe_item.attrib.get('name'))
        return cpe_names

    def parse_cpe_name(self, cpe_item):
        return cpe_item.str.split(':')

    def get_all_titles_text(self):
        titles_text = []
        for cpeItem in self.get_all_cpe_items():
            titles_text.append(cpeItem.find('title', self.namespaces).text)
        return titles_text

    def get_all_references_text(self):
        references = []
        for rfs in self.get_all_cpe_items():
            try:
                references.append([x.attrib for x in
                                   rfs.find('references', self.namespaces).findall('reference', self.namespaces)])
            except AttributeError:
                references.append([])
        return references

    def get_all_cpe23_names(self):
        cpe_23_names = []
        for cpeItem in self.get_all_cpe_items():
            cpe_23_names.append(
                cpeItem.find('{http://scap.nist.gov/schema/cpe-extension/2.3}cpe23-item').attrib.get('name'))
        return cpe_23_names

    def fit_cpe_to_software(self, prog_name):
        for cpe_item in self.get_all_cpe_items():
            if prog_name in cpe_item.find('title', self.namespaces).text:
                return cpe_item




if __name__ == "__main__":
    cpe_xml = CpeXmlParser(cpe_xml_file_name)
    titles = cpe_xml.get_all_titles_text()
    cpe_items = cpe_xml.get_all_cpe_items_names()
    cpe_23_names = cpe_xml.get_all_cpe23_names()
    cpe_references = cpe_xml.get_all_references_text()
    finall_df = pd.DataFrame([titles, cpe_items, cpe_23_names, cpe_references]).transpose()
    finall_df.columns = ['titles', 'cpe_items', 'cpe_23_names', 'cpe_references']
    splited = finall_df['cpe_23_names']
    new_splited_columns = ['cpe', 'cpe_version', 'part', 'vendor', 'product', 'version', 'update', 'edition',
                           'language',
                           'sw_edition', 'target_sw', 'target_hw', 'other']
    finall_df[new_splited_columns] = splited
    finall_df = finall_df.drop(['cpe'], axis=1)
    finall_df.to_csv("parsed_xml.csv")

    data_access = CpePdDataAccess(parsed_cpe_csv_file_name, reg_data_file_name)
    res = data_access.find_cpe_by_software("Python Software Foundation", "3.1.9.0", "Python 3.9.5 pip Bootstrap (64-bit)")
    print(res)