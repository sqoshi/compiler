import ply.yacc

from src.lexer import lexer, tokens

variables = {}


def begin(string: str) -> str:
    return "BEGIN {} \n".format(string)


def end(string: str) -> str:
    return "END {} \n".format(string)


def p_NUM(p):
    '''value : NUM '''
    p[0] = ("num", p[1])


def p_identifier(p):
    '''value : identifier '''
    p[0] = (p[1])


def p_program(p):
    '''program : '''
    p[0] = 'HALT'


def p_error(p):
    raise Exception("Line {} error string {} is not recognized ".format(p.lineno, p.value))


parser = ply.yacc.yacc()


def test_compiler(f1='../test', f2='result.mr'):
    f = open(f1, "r")
    print('x')
    parsed = parser.parse(f.read(), tracking=True)
    print('x')
    fw = open(f2, "w")
    print('x')
    fw.write(parsed)


test_compiler()
