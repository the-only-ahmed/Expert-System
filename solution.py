from parser import *
from implication import *

def solve(variables, rules, queries):
    ln = len(rules)
    essai = 0
    while len(rules) > 0 and checkQuery():
        for rule in rules:
            if len([item for item in rule if item[1] == IMP]) > 0:
                if solveRule(rule, essai):
                    rules.remove(rule)
            else:
                print IFOF + " is currently not available"
                exit()
        if ln == len(rules):
            essai += 1
            if essai > 1:
                break
        elif essai > 0:
            essai = 0
        ln = len(rules)
    for q in queries:
        if queries[q] is None:
            queries[q] = False
    print queries

def checkQuery():
    for q in queries:
        if queries[q] is None:
            return True
    return False
