import pandas as pd
import json

files_name = ["nvdcve-1.1-2002.json"]
for file_name in files_name:
    with open("nvd\\{}".format(file_name)) as f:
        cve = json.load(f)
