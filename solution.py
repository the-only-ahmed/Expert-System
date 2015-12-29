from parser import *
from implication import *
from ifof import *

def solve(rules, verbose, undet):
    ln = len(rules)
    essai = 0

    for q in queries:
        if variables[q] is not None:
            queries[q].append(variables[q])
    while len(rules) > 0:
        delete = []
        rules = reorganize(rules, verbose)
        for rule in rules:
            if (verbose):
                print "rule : " + str(rule)
                print "variables : " + "\033[92m" + str(variables) + "\033[0m"
                print "queries" + "\033[92m" + str(queries) + "\033[0m"
            if len([item for item in rule if item[1] == IMP]) > 0:
                if solveRule(rule, essai, verbose, undet):
                    delete.append(rule)
                    essai = 0
            elif len([item for item in rule if item[1] == IFOF]) > 0:
                if solveIfof(rule, verbose, undet):
                    essai = 0
                    delete.append(rule)
            else:
                print "ERROR"
                exit()
        for d in delete:
            if d in rules:
                rules.remove(d)
        if ln == len(rules):
            essai += 1
            if essai > 1:
                break
        elif essai > 0:
            essai = 0
        ln = len(rules)
    printResult(undet)

def printResult(undet):
    queries = setQueries(undet)
    for q in queries:
        if queries[q] is None:
            print '\033[1m' + '\033[93m' + str(q) + "\033[94m is undetermined\033[0m"
        elif queries[q] is True:
            print '\033[1m' + '\033[93m' + str(q) + "\033[92m is " + str(queries[q]) + "\033[0m"
        else:
            print '\033[1m' + '\033[93m' + str(q) + "\033[91m is " + str(queries[q]) + "\033[0m"

def setQueries(undet):
    result = {}
    for q in queries:
        if len(queries[q]) > 0:
            if len(list(set(queries[q]))) > 1 and undet:
                result[q] = None
            else:
                result[q] = queries[q][0]
        else:
            if (undet):
                result[q] = None
            else:
                result[q] = False
    return result

def getPerc(rule):
    leftSide = []
    for item in rule:
        if item[1] in [IMP, IFOF]:
            break
        else:
            leftSide.append(item)
    leftVars = [item for item in leftSide if item[1] == VAR]
    known = len([item for item in leftVars if variables[item[0]] is not None])

    return (known * 100) / len(leftVars)

def reorganize(rules, verbose):
    if verbose:
        print "sorting rules according to known variables so we can get a better solve of the problem"
    rl = []
    for rule in rules:
        rl.append((rule, getPerc(rule)))
    rl = sorted(rl, key=lambda x: x[1], reverse=True)
    rules = []
    for rule in rl:
        rules.append(rule[0])
    return rules
