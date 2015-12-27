from parser import *
from implication import *
from ifof import *

def solve(variables, rules, queries):
    ln = len(rules)
    essai = 0

    # setVariables()
    # print variables
    for q in queries:
        if variables[q] is not None:
            queries[q].append(variables[q])
    while len(rules) > 0:#  and checkQuery():
        delete = []
        for rule in rules:
            if len([item for item in rule if item[1] == IMP]) > 0:
                if solveRule(rule, essai):
                    # print "rule to remove : " + str(rule)
                    delete.append(rule)
                    # rules.remove(rule)
            elif len([item for item in rule if item[1] == IFOF]) > 0:
                if solveIfof(rule, essai):
                    delete.append(rule)
                    # rules.remove(rule)
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
    # print variables
    # # for q in queries:
    # #     if queries[q] is None:
    # #         queries[q] = [False]
    print queries

def checkQuery():
    for q in queries:
        if queries[q] is None:
            return True
    return False

def setVariables():
    for v in variables:
        if variables[v] is None and v not in queries:
            variables[v] = False
