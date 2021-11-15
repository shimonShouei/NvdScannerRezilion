import xml.etree.ElementTree as ET

tree = ET.parse('official-cpe-dictionary_v2.3.xml')
root = tree.getroot()
elemList = []
for elem in root.iter():
    elemList.append(elem.tag)
# now I remove duplicities - by convertion to set and back to list
elemList = list(set(elemList))
# Just printing out the result
print(elemList)