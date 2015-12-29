from parser import *

def solveRule(rule, essai, verbose, undet):
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
    global variables
    if (verbose):
        print "\033[91m" + str(leftSide) + " => " + "\033[95m" + str(left) + "\033[0m"
    if left is None:
        if essai == 1:
            if (verbose):
                print "supposing that the unknown variables in the leftSide are False"
            #global variables
            tmp = dict(variables)
            leftVars = [item[0] for item in leftSide if item[1] == VAR]
            for v in leftVars:
                if variables[v] is None:
                    variables[v] = False
            left = solveSide(leftSide)
            variables = dict(tmp)
            if left is None:
                return False
        else:
            return False
    if setOtherSide(rightSide, left, verbose, undet) is None:
        return False
    return True

def setOtherSide(sideLst, left, verbose, undet):
    unknownLst = [item for item in sideLst if item[1] == VAR and variables[item[0]] == None]
    if (verbose):
        print "unknown variables : " + str(unknownLst)
    if len(unknownLst) == 1:
        unknown = unknownLst[0][0]
        val = solveSide(sideLst, left)
        if (verbose):
            print str(unknown) + " => " + str(val)
        if unknown in queries:
            queries[unknown].append(val)
        elif not undet:
            variables[unknown] = val
        return True
    elif len(unknownLst) > 1:
        if left is not None:
            notLst = []
            no = False
            for x in sideLst:
                if x[1] == OP and x[0] != '+':
                    if (verbose):
                        print "the unknow variables could be true and false"
                    return None
                elif x[1] == NOT:
                    no = True
                elif x[1] == VAR and no:
                    notLst.append(x[0])
                    no = False
            for uk in unknownLst:
                v = left
                if uk[0] in notLst:
                    v = not left
                if (verbose):
                    print str(uk[0]) + " => " + str(v)
                if uk[0] in queries:
                    queries[uk[0]].append(v)
                elif not undet:
                    variables[uk[0]] = v
            return True
        else:
            if (verbose):
                print "could not find the unknown variables, will recheck later"
            return None
    else:
        if (verbose):
            print "there is no unknown variable in this Side of the rule"
        return False

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
            finalRes = None
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
                        if res is True:
                            finalRes = True
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
                        if res is True:
                            finalRes = True
                        res = res or v
                    elif op == '^':
                        res = res ^ v
                    else:
                        res = v
                pos += 1
            if finalRes is not None:
                res = finalRes
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
