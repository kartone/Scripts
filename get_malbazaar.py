import requests
import json


data = { 'query': 'get_taginfo', 'tag': 'Sodinokibi'}
response = requests.post('https://mb-api.abuse.ch/api/v1/', data = data, timeout=10)
maldata = response.json()
#print(json.dumps(maldata, indent=2, sort_keys=False))

for key in maldata:
    value = maldata[key]
    print("The key and value are ({}) = ({})".format(key, value))