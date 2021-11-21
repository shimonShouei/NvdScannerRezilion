import xml.etree.ElementTree as et
# import pandas as pd

# namespaces = {'': 'http://cpe.mitre.org/dictionary/2.0',
#                   'xsi': "http://www.w3.org/2001/XMLSchema-instance",
#                   'scap-core': "http://scap.nist.gov/schema/scap-core/0.3",
#                   'cpe-23': "http://scap.nist.gov/schema/cpe-extension/2.3",
#                   "ns6": "http://scap.nist.gov/schema/scap-core/0.1",
#                   'meta': "http://scap.nist.gov/schema/cpe-dictionary-metadata/0.2"}
# df = pd.read_xml('official-cpe-dictionary_v2.3TESTS.xml', xpath='//cpe-23:cpe23-item', namespaces=namespaces)
# splited = df['name'].str.split(':', n=12, expand=True)
# new_splited_columns = ['cpe', 'cpe_version', 'part', 'vendor', 'product', 'version', 'update', 'edition', 'language',
#                        'sw_edition', 'target_sw', 'target_hw', 'other']
# df[new_splited_columns] = splited
# df = df.drop(['deprecation', 'cpe'], axis=1)
# # df.to_csv('official-cpe-dictionary_v2.3.csv')
#
# x = df[df['product'] == 'form_maker']
# print(x)


class CpeXml:
    namespaces = {'': 'http://cpe.mitre.org/dictionary/2.0',
                  'xsi': "http://www.w3.org/2001/XMLSchema-instance",
                  'scap-core': "http://scap.nist.gov/schema/scap-core/0.3",
                  'cpe-23': "http://scap.nist.gov/schema/cpe-extension/2.3",
                  "ns6": "http://scap.nist.gov/schema/scap-core/0.1",
                  'meta': "http://scap.nist.gov/schema/cpe-dictionary-metadata/0.2"}
    file_name = 'official-cpe-dictionary_v2.3TESTS.xml'

    def __init__(self, file_name):
        self.tree = et.parse(file_name)
        self.root = self.tree.getroot()

    def get_all_cpe_items(self):
        return self.root.findall('cpe-item', self.namespaces)

    def get_all_cpe_items_names(self):
        cpe_names = []
        for cpe_item in self.get_all_cpe_items():
            cpe_names.append(cpe_item.attrib.get('name'))

    def parse_cpe_name(self, cpe_item):
        return cpe_item.str.split(':')

    def get_all_titles_text(self):
        titles_text = []
        for cpeItem in self.get_all_cpe_items():
            titles_text.append(cpeItem.find('title', self.namespaces).text)
        return titles_text

    def string_to_cpe(self, prog_name):
        for cpe_item in self.get_all_cpe_items():
            if prog_name in cpe_item.find('title', self.namespaces).text:
                return cpe_item











