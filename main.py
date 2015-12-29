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
    parser.add_argument("-v", "--verbose", help="feedback to explain the answer", action="store_true")
    parser.add_argument("-s", "--facts", help="set new facts for the same rules", action="store_true")
    parser.add_argument("-u", "--undetermined", help="check if variable is undetermined or not", action="store_true")
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
    else:
        print "fd is None"
        exit()

    if (args.facts):
        setNewFacts(rules, args.verbose, args.undetermined)
    else:
        solve(rules, args.verbose, args.undetermined)

def deleteAll():
    for v in variables:
        variables[v] = None
    for q in queries:
        queries[q] = []

def setNewFacts(rules, verbose, undet):
    try:
        while (True):
            print rules
            deleteAll()
            var = raw_input("\033[35menter the new Facts : \033[0m").strip()
            exist = True
            for c in var:
                if c not in variables:
                    exist = False
                    print str(c) + " doesn't exist"
                    break
                else:
                    variables[c] = True
            if not exist:
                continue
            solve(rules, verbose, undet)
    except:
        print "bye"

main()
