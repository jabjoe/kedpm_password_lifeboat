#! /usr/bin/python2
from kedpm.plugins.pdb_figaro import PDBFigaro, FigaroPassword
import getpass
import sys
import os

f = os.path.join(os.environ["HOME"],".fpm/fpm")

if len(sys.argv) > 1:
    f = sys.argv[1]

db = PDBFigaro(filename=f)

pw = getpass.getpass('Please give password : ')

db.open(pw)

tree = db.getTree()


header = [ f[1]['title'] for f in FigaroPassword.fields_type_info ]
print "Path,", ",".join(header)


def dump_tree(p, t):
    for n in t.getNodes():
        print "%s," % p, n.asCSV()

    branches = t.getBranches()

    for k in branches:
        dump_tree("%s%s/" % (p, k), branches[k])

dump_tree("/", tree)
