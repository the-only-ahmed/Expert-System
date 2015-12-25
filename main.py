#!/usr/bin/env python
import os
import os.path
import sys
import argparse
from parser import *
from solution import solve

def check_fileExistance(path):
    if os.path.isfile(path):
        if os.access(path, os.R_OK):
            fd = open(path, 'r')
            return fd
        else:
            print("File can't be opened")
            exit()
    else:
        print("File doesn't exist")
        exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--colors", help="add colors to shell", nargs=1)
    parser.add_argument("-f", "--file", help="add configuration file", nargs=1)
    args = parser.parse_args()
    fd = None
    if (args.file != None):
        fd = check_fileExistance(args.file[0])
    else:
        print "usage: " + sys.argv[0] + " [-h] [-c COLORS] [-f FILE]"
        exit()
    if fd is not None:
        parse_file(fd)

    solve(variables, rules, queries)

main()
