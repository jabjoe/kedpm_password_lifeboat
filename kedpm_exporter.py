#! /usr/bin/python2
from kedpm.plugins.pdb_figaro import PDBFigaro, FigaroPassword
import getpass
import sys
import os
import json

f = os.path.join(os.environ["HOME"],".fpm/fpm")

if len(sys.argv) > 1:
    f = sys.argv[1]

db = PDBFigaro(filename=f)

pw = getpass.getpass('Please give password : ')

db.open(pw)

tree = db.getTree()

def get_tree(t):
    files = {}
    for n in t.getNodes():
        files[n['title']] = { 'user': n['user'],
                          'password' : n['password'],
                          'url' : n['url'],
                          'notes' : n['notes']}

    branches = t.getBranches()
    folders = {}

    for k in branches:
        folders[k] = get_tree(branches[k])
    return {'files': files, 'folders': folders}

d = get_tree(tree)

json.dump(d, open("passwords.json", "w"))
