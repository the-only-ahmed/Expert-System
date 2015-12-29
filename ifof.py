from parser import *
from implication import *

def solveIfof(rule, verbose, undet):
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
    right = solveSide(rightSide)
    if (verbose):
        print "\033[92m" + str(leftSide) + " => " + "\033[95m" + str(left) + "\033[0m"
        print "\033[92m" + str(rightSide) + " => " + "\033[95m" + str(right) + "\033[0m"
    if left is None and right is None:
        return None
    elif left is None and right is not None:
        if setOtherSide(leftSide, right, verbose, undet) is None:
            return False
    elif left is not None and right is None:
        if setOtherSide(rightSide, left, verbose, undet) is None:
            return False
    return True

    #
    # if left is None:
    #     global variables
    #     tmp = dict(variables)
    #     leftVars = [item[0] for item in leftSide if item[1] == VAR]
    #     for v in leftVars:
    #         if variables[v] is None:
    #             variables[v] = False
    #     left = solveSide(leftSide)
    #     variables = dict(tmp)
    #     if left is None:
    #         return False
    # if setOtherSide(rightSide, left, essai) is None:
    #     return False
    # return True
