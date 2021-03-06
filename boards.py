#!/usr/local/bin/python 

import argparse
import csv
import json
import requests
import urllib
import sys
import yaml

from string import Template


parser = argparse.ArgumentParser(description='Trello boards.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--org', type=str, 
                    help='Name of org', 
                    default='udemy')

args = parser.parse_args()

keys = yaml.load(open("keys.yml", 'r'))
key= keys['Key']
token = keys['Secret']
org=urllib.quote(args.org)

t = Template('https://api.trello.com/1/organizations/$org/boards?key=$key&token=$token')

url = t.substitute(key=key, token=token, org=org)

r = requests.get(url)

for board in r.json():
    print unicode(board['name']).encode('utf8')

