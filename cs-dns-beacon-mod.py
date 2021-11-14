#!/usr/bin/env python

from __future__ import print_function

__description__ = 'Get Cobalt Strike DNS beacon'
__author__ = 'Didier Stevens'
__modified_by__ = 'Mario Ciccarelli'
__version__ = '0.0.1'
__date__ = '2021/11/14'
__blog__ = ''

import string
import sys
import dns.resolver
import argparse
from tenacity import *

class MyException(Exception):
    pass

#https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
def int2base(x, base, leading=0):
    digs = string.ascii_letters

    if x < 0:
        sign = -1
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    while len(digits) < leading:
        digits.append(digs[0])

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

@retry
def query_dns(r,q):
    try:
        print('[+] Dumping stage: {}'.format(q))
        t = r.resolve(q, 'txt')[0].to_text().strip('"')
    except Exception as e:
        print('Failed at: '+ str(e) + ' retrying...')
        raise Exception
    return t

def Main(ipv4, domain, filename):
    counter = 0
    alltext = ''
    oResolver = dns.resolver.Resolver()
    oResolver.nameservers = [ipv4]
    while True:
        query = int2base(counter, 26, 3)[::-1] + '.' + domain + '.'
        text = query_dns(oResolver,query)
        if text == '':
            print("TXT record empty")
            break
        counter += 1
        alltext += text
    with open(filename, 'w') as fOut:
        fOut.write(alltext)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Cobalt Strike DNS beacon')
    parser.add_argument('ip_address',  help='DNS server address, can be the CS Team Server directly')
    parser.add_argument('domain',  help='Domain name of CS beacon')
    parser.add_argument('output_file', help='Output dump file')
    args = parser.parse_args()

    ipv4 = args.ip_address
    outfile = args.output_file
    domain = args.domain

    #domain = 'stage.whatever.domain'

    Main(ipv4, domain, outfile)
