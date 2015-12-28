from parser import *
from implication import *
from ifof import *

def solve(variables, rules, queries):
    ln = len(rules)
    essai = 0

    for q in queries:
        if variables[q] is not None:
            queries[q].append(variables[q])
    while len(rules) > 0:
        delete = []
        rules = reorganize(rules)
        for rule in rules:
            if len([item for item in rule if item[1] == IMP]) > 0:
                if solveRule(rule, essai):
                    delete.append(rule)
                    essai = 0
            elif len([item for item in rule if item[1] == IFOF]) > 0:
                if solveIfof(rule):
                    essai = 0
                    delete.append(rule)
            else:
                print IFOF + " is currently not available"
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
    # # for q in queries:
    # #     if queries[q] is None:
    # #         queries[q] = [False]
    queries = setQueries()
    # queries = checkQuery()
    print queries

def setQueries():
    result = {}
    for q in queries:
        result[q] = queries[q][0]
    return result

def checkQuery():
    result = {}
    for q in queries:
        if len(list(set(queries[q]))) > 1 or len(queries[q]) == 0:
            result[q] = None
        else:
            result[q] = queries[q][0]
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

def reorganize(rules):
    rl = []
    for rule in rules:
        rl.append((rule, getPerc(rule)))
    rl = sorted(rl, key=lambda x: x[1], reverse=True)
    rules = []
    for rule in rl:
        rules.append(rule[0])
    return rules
