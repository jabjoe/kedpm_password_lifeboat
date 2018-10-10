#! /usr/bin/python3
import hashlib
import json

d = json.load(open("passwords.json", "r"))


def convert_to_csv(folder_in, path, parent_label, parent_id, folders_csv, files_csv):
    files = folder_in['files']
    folders = folder_in['folders']

    for name in files:
        e = files[name]
        files_csv.writelines([ '"%s", "%s" , "%s", "%s", "%s", "%s", "%s"\n' % (
                     parent_id,
                     parent_label,
                     name,
                     e['user'],
                     e['password'],
                     e['url'],
                     e['notes'])])

    for name in folders:
        folder = folders[name]
        folder_path = path + "/" + name
        m = hashlib.sha1()
        m.update(b"folder")
        m.update(bytes(folder_path, encoding='utf-8'))
        folder_id = m.hexdigest()
        folders_csv.writelines([ '"%s", "%s", "%s"  , "%s"\n' % (folder_id, parent_id, parent_label, name) ])
        convert_to_csv(folder, folder_path, name, folder_id, folders_csv, files_csv)


nc_pw_files = open("nc_pw_passwords.csv", "w")
nc_pw_dirs  = open("nc_pw_folders.csv", "w")

nc_pw_files.writelines([ 'folder_id, folder, label , username, password, url, notes\n' ])
nc_pw_dirs.writelines([ 'id, parent_id , parent_label, label\n' ])

m = hashlib.sha1()
m.update(b"folder")
m.update(b"root")
root_id = m.hexdigest()

convert_to_csv(d, "root", "root", root_id, nc_pw_dirs, nc_pw_files)
