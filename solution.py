from parser import *

def solve(variables, rules, queries):
    for rule in rules:
        if len([item for item in rule if item[1] == IMP]) > 0:
            if solveRule(rule):
                rules.remove(rule)
        else:
            print IFOF + " is currently not available"
            exit()

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
    if len(unknownLst) > 1:
        return None
    unknown = unknownLst[0][0]
    print unknown + " in " + str(sideLst)

def solveSide(sideLst):
    op = None
    var = None
    no = False
    res = None

    for item in sideLst:
        if item[1] == NOT:
            no = True
        elif item[1] == OP:
            op = item[0]
        elif item[1] == VAR:
            if variables[item[0]] is None:
                return None
            elif res is None:
                v = variables[item[0]]
                if no:
                    v = not v
                    no = False
                res = v
            else:
                v = variables[item[0]]
                if no:
                    v = not v
                    no = False
                if op == '+':
                    res = res and v
                elif op == '|':
                    res = res or v
                else:
                    res = res ^ v
    return res
