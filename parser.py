import lexer

OP = 'operator'
NOT = 'Not'
PAR = 'Parenthesis'
THEN = 'Implication'
FACT = 'Fact'
QUR = 'Query'
VAR = 'Variable'

token_exprs = [
    (r'\<=>', THEN),
    (r'\=>', THEN),
    (r'\?', QUR),
    (r'\=', FACT),
    (r'\(', PAR),
    (r'\)', PAR),
    (r'\+', OP),
    (r'\^', OP),
    (r'\|', OP),
    (r'\!', NOT),
    (r'[A-Za-z]', VAR),
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs)

rules = []
queries = []
variables = {}

def checkSides(sideLst):
    OpNb = len([item for item in sideLst if item[1] == OP]) + 1
    VarNb = len([item for item in sideLst if item[1] == VAR])
    ParNb = len([item for item in sideLst if item[1] == PAR])
    if OpNb != VarNb or ParNb % 2 != 0:
        return False

    last_T = None
    parNb = 0
    parChar = None

    if sideLst[0][1] == OP or sideLst[-1][1] in [OP, NOT]:
        return False

    for item in sideLst:
        if last_T is not None:
            if last_T == item[1] or (last_T == VAR and item[1] == NOT):
                return False
            elif item[1] == OP and last_T not in [VAR, PAR]:
                return False
            elif item[1] == PAR:
                if item[0] == "(" and last_T != OP:
                    return False
                elif item[0] == ")" and last_T != VAR:
                    return False
            elif last_T == PAR:
                if parChar is not None:
                    if parChar == "(" and item[1] is not VAR:
                        return False
                    if parChar == ")" and item[1] is not OP:
                        return False
        if item[1] == PAR:
            parChar = item[0]
            if item[0] == "(":
                parNb += 1
            else:
                if parNb <= 0:
                    return False
                parNb -= 1
        last_T = item[1]

    if parNb != 0:
        return False
    return True

def parse_RulesError(lex):
    if len([item for item in lex if item[1] == THEN]) != 1:
        return False
    if lex[0][1] == THEN or lex[-1][1] == THEN:
        return False

    leftSide = []
    rightSide = []
    isImp = False
    for item in lex:
        if item[1] == VAR:
            if item[0] not in variables:
                variables[item[0]] = False
        if item[1] in [QUR, FACT]:
            return False
        if item[1] == THEN:
            isImp = True
        elif not isImp:
            leftSide.append(item)
        else:
            rightSide.append(item)

    return (checkSides(leftSide) and checkSides(rightSide))

def parse_Error(lex, State):
    if len([item for item in lex if item[1] == State]) != 1:
        return False
    if len([item for item in lex if item[1] not in [State, VAR]]) != 0:
        return False
    var = [item for item in lex if item[1] == VAR]
    if len(var) != len(set(var)):
        return False
    wrong_var = [item for item in lex if item[1] == VAR and item[0] not in variables.keys()]
    if len(wrong_var) > 0:
        print "Variables : " + wrong_var + " doesn't exist"
        return False
    return True

def parse_file(fd):
    t_list = fd.read().splitlines()
    facts = []

    for i, lines in enumerate(t_list):
        tmp = lines.strip().split("#")
        cmd = tmp[0].strip()
        if (cmd != ""):
            cmd = cmd.replace(" ", "")
            cmd = cmd.replace("\t", "")
            lexedLst = imp_lex(cmd)
            if (lexedLst[0][1] == FACT):
                if len(queries) > 0:
                    print "Parse error in Facts: Facts must always between the Rules and the Queries"
                    print "error line: " + lines
                    exit()
                if not parse_Error(lexedLst, FACT):
                    print "Parse error in Facts: " + lines
                facts.append(lexedLst)
            elif (lexedLst[0][1] == QUR):
                if len(facts) == 0:
                    print "Parse error in Query: Query must always be at the end of the file"
                    print "error line: " + lines
                    exit()
                if not parse_Error(lexedLst, QUR):
                    print "Parse error in Queries: " + lines
                queries.append(lexedLst)
            else:
                if len(facts) > 0 or len(queries) > 0:
                    print "Parse error in Rules: Rules must always be in the top of the file"
                    print "error line: " + lines
                    exit()
                if not parse_RulesError(lexedLst):
                    print "Parse error in Rules: " + lines
                    exit()
                rules.append(cmd)
    setFacts(facts)

def setFacts(facts):
    for fact in facts:
        for f in fact:
            if f[1] == VAR:
                variables[f[0]] = True
