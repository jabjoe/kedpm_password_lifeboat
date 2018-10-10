#! /usr/bin/python3

import select
import getpass
import subprocess
import termios
import tty
import pty
import sys
import os

master_fd, slave_fd = pty.openpty()

p = subprocess.Popen(["python", "/usr/bin/kedpm", "-c"], stdin=slave_fd, stdout=slave_fd, stderr=slave_fd)


def cmd_rsp(cmd, rsp_start, rsp_end):
    os.write(master_fd, str("%s\n" % cmd).encode())
    r_lines = []
    started = False
    while p.poll() is None:
        r, w, e = select.select([sys.stdin, master_fd], [], [])
        if sys.stdin in r:
            d = sys.stdin.readline().encode()
            os.write(master_fd, d)
        elif master_fd in r:
            o = os.read(master_fd, 10240)
            if o:
                o = o.decode()
                lines = o.split("\n")
                for line in lines:
                    line = line.rstrip()
                    if started:
                        if line.find(rsp_end) != -1:
                            return r_lines
                        else:
                            r_lines += [line]
                    elif line.find(rsp_start) != -1:
                        started = True
                    else:
                        print(line)



try:
    while p.poll() is None:
        r, w, e = select.select([sys.stdin, master_fd], [], [])
        if sys.stdin in r:
            d = sys.stdin.readline().encode()
            os.write(master_fd, d)
        elif master_fd in r:
            o = os.read(master_fd, 10240)
            if o:
                o = o.decode()
                if o.find("Password accepted.") != -1:
                    print(cmd_rsp("ls", "=== Directories ===", "==== Passwords ===="))
                else:
                    print(o)
except Exception as e:
    print(e)
    pass




'''
rlist = [p.stdout, p.stderr]

r = select.select(rlist,[], [])

for line in r[0][0]:
    print(line)

while True:
    line = p.stdout.readline()
    if line == "Password:":
        pw = getpass.getpass('Please give password : ')
        p.stdin.communicate(input=pw)
    else:
        print(line)
'''
