import requests
import re

r = requests.get('https://nvd.nist.gov/vuln/data-feeds#JSON_FEED')
#list = re.findall("nvdcve-1.1-[0-9]*\.json\.zip",r.text)
for filename in re.findall("nvdcve-1.1-[0-9]*\.json\.zip",r.text):
    r_file = requests.get("https://nvd.nist.gov/feeds/json/cve/1.1/" + filename, stream=True)
    with open("nvd/" + filename, 'wb') as f:
        for chunk in r_file:
            f.write(chunk)