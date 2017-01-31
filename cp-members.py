#!/usr/local/bin/python 

import argparse
import csv
import json
import requests
import urllib
import sys
import yaml

from string import Template


parser = argparse.ArgumentParser(description='Trello board membership tool.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--dryrun', action='store_true', 
                    help='Just list the users', 
                    default=False)
parser.add_argument('--boardID', type=str, 
                    help='Board ID', 
                    default='bdpGLeHh') # Trello Testing Sandbox board
parser.add_argument('--sourceBoardID', type=str, 
                    help='Board ID', 
                    default='wmemgG44') # default is a webapp team T board

args = parser.parse_args()


keys = yaml.load(open("keys.yml", 'r'))
key= keys['Key']
secret = keys['Secret']
token = keys['Token']
boardID=urllib.quote(args.boardID)
sourceBoardID=urllib.quote(args.sourceBoardID) 

print 'Adding members to' + ' "' + args.boardID + '" from "' + sourceBoardID + '"'

t = Template('https://trello.com/1/board/$sourceBoardID/members?filter=admins&key=$key&token=$token')
url = t.substitute(key=key, token=secret, sourceBoardID=sourceBoardID)
admins = requests.get(url).json()

t = Template('https://trello.com/1/board/$sourceBoardID/members?filter=normal&key=$key&token=$token')
url = t.substitute(key=key, token=secret, sourceBoardID=sourceBoardID)
users = requests.get(url).json()

print 'Admins'
for admin in admins:
    print ' ' + admin[u'username']
    if args.dryrun:
        continue
    t = Template('https://trello.com/1/board/$boardID/members/$member?key=$key&token=$token&type=admin')
    url = t.substitute(key=key, token=token, boardID=boardID, member=admin[u'id'])
    r = requests.put(url)
    if r.status_code != 200:
        print r
        sys.exit
    
print 'Normal Users'
for user in users:
    print ' ' + user[u'username']
    if args.dryrun:
        continue
    t = Template('https://trello.com/1/board/$boardID/members/$member?key=$key&token=$token&type=normal')
    url = t.substitute(key=key, token=token, boardID=boardID, member=user[u'id'])
    r = requests.put(url)
    if r.status_code != 200:
        print r
        sys.exit
