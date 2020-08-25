# Testing malware bazaar API
# Test

import requests
import json


data = { 'query': 'get_taginfo', 'tag': 'Sodinokibi'}
response = requests.post('https://mb-api.abuse.ch/api/v1/', data = data, timeout=10)
maldata = response.json()
#print(json.dumps(maldata, indent=2, sort_keys=False))

key=0
while True:
  try: 
    value = maldata["data"][key]["sha256_hash"]
    print("The key and value are ({}) = ({})".format(key, value))
    key+=1
  except IndexError:
    break