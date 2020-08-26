# Testing Malware Bazaar API

import requests
import json
import os, glob
import pyzipper

KEY = os.environ.get("API_KEY")
ZIP_PASSWORD = b"infected"
EXT_TO_CLEAN = "zip"

def housekeeping(ext):
    try:
        for f in glob.glob('*.'+ext):
            os.remove(f)
    except OSError as e:
        print("Error: %s - %s " % (e.filename, e.strerror))

def get_sample(hash):
    headers = { 'API-KEY': KEY } 
    data = { 'query': 'get_file', 'sha256_hash': hash }
    response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, headers=headers, allow_redirects=True)
    with open(hash+'.zip', 'wb') as f:
        f.write(response.content)
        print("[+] Sample downloaded successfully")
    with pyzipper.AESZipFile(hash+'.zip') as zf:
        zf.extractall(path=".", pwd=ZIP_PASSWORD)
        print("[+] Sample unpacked successfully")

def main():
    downloaded_sample = []
    data = { 'query': 'get_taginfo', 'tag': 'Sodinokibi' }
    response = requests.post('https://mb-api.abuse.ch/api/v1/', data = data, timeout=10)
    maldata = response.json()
    #print(json.dumps(maldata, indent=2, sort_keys=False))
    print("[+] Retrieving the list of downloaded samples...")
    for file in glob.glob("./samples/*.exe"):
        filename = file.rstrip(".exe").lstrip("./samples/")
        downloaded_sample.append(filename)
    print(downloaded_sample)
    for i in range(len(maldata["data"])):
        if "Decryptor" not in maldata["data"][i]["tags"]:
            for key in maldata["data"][i].keys():
                if key == "sha256_hash":
                    value = maldata["data"][i][key]
                    if value not in downloaded_sample:
                        print("[+] Downloading sample with ", key, "->", value)
                        #get_sample(value)
                        #housekeeping(EXT_TO_CLEAN)
        else:
            print("[+] Skipping the sample because of Tag: Decryptor")
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass