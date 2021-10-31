from os import listdir
from os.path import isfile, join
import zipfile
import json

files = [f for f in listdir("nvd/") if isfile(join("nvd/", f))]
files.sort()
for file in files:
    archive = zipfile.ZipFile(join("nvd/", file), 'r')
    jsonfile = archive.open(archive.namelist()[0])
    cve_dict = json.loads(jsonfile.read())
    jsonfile.close()