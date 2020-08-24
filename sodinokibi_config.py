"""Extract Sodinokibi ransomware configuration from a given exe/folder of exes"""
import os
import sys
import scandir
import pefile
import string
import struct
import json
from Crypto.Cipher import ARC4

def arc4(key, enc_data):
    var = ARC4.new(key)
    dec = var.decrypt(enc_data)
    return dec

def extract_sodinokibi_config(filename):
    print(filename)
    try:
        pe = pefile.PE(filename)
        section = pe.sections[3]
        data = section.get_data()
        enc_len = struct.unpack('I', data[0x24:0x28])[0]
        dec_data = arc4(data[0:32], data[0x28:enc_len + 0x28])
        parsed = json.loads(dec_data[:-1])
        print(json.dumps(parsed, indent=2, sort_keys=True))
    except Exception as e:
        print("ERROR - {}".format(e))

def main():
    if os.path.isdir(sys.argv[1]):
            for root, dirs, files in scandir.walk(sys.argv[1]):
                for file in files:
                    extract_sodinokibi_config(os.path.join(root, file))
    else:
        extract_sodinokibi_config(sys.argv[1])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass