#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys, getopt
import struct
import argparse
import shutil
import binascii


def copyFile(src):
    dest = src[:src.find(".")] + "_" + "encoded" + ".exe"
    print("File {0} created".format(dest))
    try:
        shutil.copy(src, dest)
    except IOError, e:
        print "Unable to copy file. %s" % e
        sys.exit()
    return dest


def main():
    """ Main program """
    # Code goes over here.

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--filename", help="File to encode", type=str)
    parser.add_argument("-i","--init", help="The offset from which the encoding starts, e.g. 0x3e05", type=lambda x: int(x,0), default=0x3e05)
    parser.add_argument("-s","--stop", help="The offset where the encoding stops, e.g. 0x996b", type=lambda x: int(x,0), default=0x996b)
    parser.add_argument("-k","--key", help="The initial key used to xor the first byte, e.g. 0xfe", type=lambda x: int(x,0), default=0xfe)
    args=parser.parse_args()

    file_to_encode = args.filename
    start_offset = args.init
    stop_offset = args.stop
    xor_key = args.key

    size = stop_offset - start_offset

    # print(str(size))

    file_encoded = copyFile(file_to_encode)
    out = []
    out.append(xor_key)

    with open(file_to_encode, "rb") as r, open(file_encoded, "r+b") as w:
        r.seek(start_offset,0)
        w.seek(start_offset,0)
        for i in range(0, size):
            b1 = ord(r.read(1)) ^ out[i]
            out.append(b1)
            w.write(struct.pack('<B', b1))
        r.close()
        w.close()
    return 0

if __name__ == "__main__":
    main()
