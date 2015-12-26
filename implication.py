from parser import *

def solveRule(rule, essai):
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
    elif setOtherSide(rightSide, left, essai) is None:
        return False
    return True

def setOtherSide(sideLst, left, essai):
    unknownLst = [item for item in sideLst if item[1] == VAR and variables[item[0]] == None]
    if len(unknownLst) == 1:
        unknown = unknownLst[0][0]
        variables[unknown] = solveSide(sideLst, left)
        queries[unknown] = variables[unknown]
        return True
    elif essai == 0:
        return None
    else:
        if left is True:
            notLst = []
            no = False
            for x in sideLst:
                if x[1] == OP and x[0] != '+':
                    return None
                elif x[1] == NOT:
                    no = True
                elif x[1] == VAR and no:
                    notLst.append(x[0])
                    no = False
            for uk in unknownLst:
                v = True
                if uk[0] in notLst:
                    v = False
                variables[uk[0]] = v
                queries[uk[0]] = v
        else:
            return None

def solveSide(*args):
    op = None
    var = None
    no = False

    supp = [True, False]
    wantedRes = None
    i = 0

    sideLst = args[0]
    if len(args) == 2:
        wantedRes = args[1]

    try :
        for i in range(len(args)):
            res = None
            pos = 0
            ignore = 0
            for item in sideLst:
                if ignore > 0:
                    ignore -= 1
                    pos += 1
                    continue
                if item[1] == PAR and item[0] == '(':
                    parLst = getParLst(sideLst, pos)
                    subCalc = solveSide(parLst)
                    ignore = len(parLst) + 1
                    if op == '+':
                        res = res and subCalc
                    elif op == '|':
                        res = res or subCalc
                    elif op == '^':
                        res = res ^ subCalc
                    else:
                        res = subCalc
                elif item[1] == NOT:
                    no = True
                elif item[1] == OP:
                    op = item[0]
                elif item[1] == VAR:
                    v = variables[item[0]]
                    if v is None:
                        if wantedRes is not None:
                            v = supp[i]
                    if no:
                        v = not v
                        no = False
                    if op == '+':
                        res = res and v
                    elif op == '|':
                        res = res or v
                    elif op == '^':
                        res = res ^ v
                    else:
                        res = v
                pos += 1
            if wantedRes is not None and res == wantedRes:
                res = supp[i]
                break
            i += 1
    except:
        return None
    return res

def getParLst(lst, pos):
    i = 0
    p = 0
    newLst = []

    for x in lst:
        if i < pos:
            i += 1
            continue
        if x[1] == PAR:
            if x[0] == '(':
                p += 1
            else:
                p -= 1
        else:
            newLst.append(x)
        if p == 0:
            return newLst
