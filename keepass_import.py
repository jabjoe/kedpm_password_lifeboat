#! /usr/bin/python3

from pykeepass import PyKeePass
import getpass
import json
import sys

f = 'db.kdbx'

if len(sys.argv) > 1:
    f = sys.argv[1]

pw = getpass.getpass('Please give password : ')

kp = PyKeePass(f, password=pw)


d = json.load(open("passwords.json", "r"))


def import_folder(folder_in, group_out):
    files = folder_in['files']
    folders = folder_in['folders']
    for name in files:
        e = files[name]
        kp.add_entry(group_out, name,
                     e['user'],
                     e['password'],
                     e['url'],
                     e['notes'])

    for name in folders:
        folder = folders[name]
        group = kp.add_group(group_out, name)
        import_folder(folder, group)


import_folder(d, kp.root_group)

kp.save()
