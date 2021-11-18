# import xml.etree.ElementTree as ET
#
# tree = ET.parse('official-cpe-dictionary_v2.3.xml')
# root = tree.getroot()
# elemList = []
# for elem in root.iter():
#     elemList.append(elem.tag)
# # now I remove duplicities - by convertion to set and back to list
# elemList = list(set(elemList))
# # Just printing out the result
# print(elemList)
import pandas as pd
namespaces = {'xsi':"http://www.w3.org/2001/XMLSchema-instance",
              'scap-core':"http://scap.nist.gov/schema/scap-core/0.3",
              'cpe-23': "http://scap.nist.gov/schema/cpe-extension/2.3",
              "ns6":"http://scap.nist.gov/schema/scap-core/0.1",
              'meta':"http://scap.nist.gov/schema/cpe-dictionary-metadata/0.2",
              'schemaLocation':"http://scap.nist.gov/schema/cpe-extension/2.3"
                               " https://scap.nist.gov/schema/cpe/2.3/cpe-dictionary-extension_2.3.xsd"
                               " http://cpe.mitre.org/dictionary/2.0"
                               " https://scap.nist.gov/schema/cpe/2.3/cpe-dictionary_2.3.xsd"
                               "http://scap.nist.gov/schema/cpe-dictionary-metadata/0.2"
                               " https://scap.nist.gov/schema/cpe/2.1/cpe-dictionary-metadata_0.2.xsd"
                               " http://scap.nist.gov/schema/scap-core/0.3"
                               " https://scap.nist.gov/schema/nvd/scap-core_0.3.xsd"
                               " http://scap.nist.gov/schema/configuration/0.1"
                               " https://scap.nist.gov/schema/nvd/configuration_0.1.xsd"
                               " http://scap.nist.gov/schema/scap-core/0.1"
                               " https://scap.nist.gov/schema/nvd/scap-core_0.1.xsd"}
df = pd.read_xml('official-cpe-dictionary_v2.3.xml', xpath='//cpe-23:cpe23-item', namespaces=namespaces)
splited = df['name'].str.split(':', n=12, expand=True)
new_splited_columns = ['cpe', 'cpe_version', 'part', 'vendor', 'product', 'version', 'update', 'edition', 'language',
                       'sw_edition', 'target_sw', 'target_hw', 'other']
df[new_splited_columns] = splited
df = df.drop(['deprecation', 'cpe'], axis=1)
df.to_csv('official-cpe-dictionary_v2.3.csv')