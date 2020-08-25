# Testing malware bazaar API

import requests
import json


data = { 'query': 'get_taginfo', 'tag': 'Sodinokibi'}
response = requests.post('https://mb-api.abuse.ch/api/v1/', data = data, timeout=10)
maldata = response.json()
#print(json.dumps(maldata, indent=2, sort_keys=False))

for i in range(len(maldata["data"])):
    for key in maldata["data"][i].keys():
        if key == "sha256_hash":
            value = maldata["data"][i][key]
            print(key, "->", value)
