from parser import *

def solve(variables, rules, queries):
    while len(rules) > 0 and checkQuery():
        for rule in rules:
            if len([item for item in rule if item[1] == IMP]) > 0:
                if solveRule(rule):
                    rules.remove(rule)
            else:
                print IFOF + " is currently not available"
                exit()
    print queries

def solveRule(rule):
    isImp = False
    leftSide = []
    rightSide = []

    for item in rule:
        if item[1] in [IMP, IFOF]:
            isImp = True
        elif not isImp:
            leftSide.append(item)
        else:
            rightSide.append(item)

    left = solveSide(leftSide)
    if left is None:
        return False
    elif setOtherSide(rightSide, left) is None:
        return False
    return True

def setOtherSide(sideLst, left):
    unknownLst = [item for item in sideLst if item[1] == VAR and variables[item[0]] == None]
    if len(unknownLst) != 1:
        return None
    unknown = unknownLst[0][0]
    variables[unknown] = solveSide(sideLst, left)
    queries[unknown] = variables[unknown]
    return True

def solveSide(*args):
    op = None
    var = None
    no = False
    res = None

    supp = [True, False]
    wantedRes = None
    i = 0

    sideLst = args[0]
    if len(args) == 2:
        wantedRes = args[1]

    try :
        for i in range(len(args)):
            for item in sideLst:
                if item[1] == NOT:
                    no = True
                elif item[1] == OP:
                    op = item[0]
                elif item[1] == VAR:
                    v = variables[item[0]]
                    if v is None:
                        if wantedRes is not None:
                            v = supp[i]
                    if res is None:
                        if no:
                            v = not v
                            no = False
                        res = v
                    else:
                        if no:
                            v = not v
                            no = False
                        if op == '+':
                            res = res and v
                        elif op == '|':
                            res = res or v
                        else:
                            res = res ^ v
            if wantedRes is not None and res == wantedRes:
                res = supp[i]
                break
            i += 1
    except:
        return None
    return res

def checkQuery():
    for q in queries:
        if queries[q] is None:
            return True
    return False
