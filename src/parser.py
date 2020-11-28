import os

import ply.yacc
import re
from src.Exceptions import *
from src.lexer import lexer, tokens

memory_counter = 1
arrays = dict()
variables = dict()
initialized = set()
labels_val = []


def clarify(text: str) -> str:
    output = ""
    for line in text.split("\n"):
        if line != '':
            output += line.lstrip() + "\n"
    return output


def get_memory_counter():
    return memory_counter


def dec_memory_counter(val=1):
    """Decrease memory counter by val(default=1)."""
    global memory_counter
    memory_counter -= val


def inc_memory_counter(val=1):
    """Increase memory counter by val(default=1)."""
    global memory_counter
    memory_counter += val


###########################################################################
######################### variable validation #############################
###########################################################################
def is_initialized(id, lineno):
    """ Check if variable was initialized. """
    if id not in initialized:
        raise VariableNotInitializedException(var=id, line_no=lineno)


def validate_var_addr(id, lineno):
    """ Check  if var was properly used and declared."""
    if id not in variables.keys():
        if id in arrays:
            raise TypeError('Error in line {}. Wrong usage of table variable {}.'.format(id, lineno))
        else:
            raise VariableNotDeclaredException(id, lineno)


def is_var_taken(id, line_no):
    """ Check if id is taken."""
    if id in variables.keys():
        raise TakenVariableNameException(var=id, line_no=line_no)


def is_var_declared(id, line_no):
    """ Check if variable were declared before use."""
    if id not in variables.keys():
        raise VariableNotDeclaredException(var=id, line_no=line_no)


def validate_indexes_array(idx1, idx2, line_no, id):
    """ Check if array indexes are valid."""
    if idx1 > idx2:
        raise IndexError('Error in line {}. Array {} indexes are wrong. ({}:{})'.format(line_no, id, idx1, idx2))


############################################################################

def add_arr(id, idx1, idx2, line_no):
    """ Save arr by id in memory and increase memory counter by array length."""
    validate_indexes_array(idx1, idx2, line_no, id)
    global memory_counter
    arrays[id] = (memory_counter + 1, idx1, idx2)
    inc_memory_counter(idx2 - idx1 + 1)


def get_var(id, line_no):
    is_var_declared(id, line_no)
    return variables[id]


def add_var(id, line_no):
    """ Save variable by id in memory and increase memory counter by 1."""
    inc_memory_counter()
    is_var_taken(id, line_no)
    variables[id] = get_memory_counter()


def rm_var(id):
    """ Remove variable from memory."""
    variables.pop(id)


def render_operation(*args):
    return ' '.join(args)


def add_nl(word):
    return str(word) + "\n"


def generate_number(number, register):
    commands = ""
    while number != 0:
        if number % 2 == 0:
            number = number // 2
            commands = render_operation("SHL", register, "\n", commands)
        else:
            number -= 1
            commands = render_operation("INC", register, "\n", commands)
    commands = render_operation("RESET", register, "\n", commands)
    return commands


def load_addr(item, lineno):
    if item[0] == "id":
        validate_var_addr(item[1], lineno)
        return generate_number(variables[item[1]], "b")


def load_value(val, register, lineno):
    if val[0] == "num":
        return generate_number(int(val[1]), register)
    if val[0] == "id":
        is_initialized(val[1], lineno)
        return load_addr(val, lineno)


##################################################################
########################### program ##############################
##################################################################
def p_program_declare(p):
    '''program  : DECLARE declarations BEGIN commands END'''
    p[0] = p[4] + "HALT"


def p_program_(p):
    '''program  : BEGIN commands END'''
    p[0] = + p[2] + "HALT"


##################################################################
###################### declarations ##############################
##################################################################

def p_declarations_variable_rec(p):
    '''declarations : declarations COMMA ID'''
    print('declarations')
    id, line_no = p[3], str(p.lineno(3))
    add_var(id, line_no)


def p_declarations_array_rec(p):
    '''declarations : declarations COMMA ID LBR NUM COLON NUM RBR'''
    print('declarations')
    add_arr(p[3], p[5], p[7], str(p.lineno(3)))


def p_declarations_variable(p):
    '''declarations : ID'''
    print('declarations')
    id, line_no = p[1], str(p.lineno(1))
    add_var(id, line_no)


def p_declarations_array(p):
    '''declarations : ID LBR NUM COLON NUM RBR'''
    print('declarations')
    add_arr(p[1], p[3], p[5], str(p.lineno(1)))


##################################################################
######################## commands ################################
##################################################################
def p_commands_multiple(p):
    '''commands : commands command'''
    p[0] = p[1] + p[2]


def p_commands_single(p):
    '''commands : command'''
    p[0] = p[1]


##################################################################
######################### command ################################
##################################################################

def p_command_assign(p):
    '''command  : identifier ASSIGN expression SEMICOLON'''
    identifier, expression, lineno = p[1], p[3], str(p.lineno(1))
    p[0] = str(expression) + load_addr(identifier, lineno) + "STORE a b\n"
    initialized.add(identifier[1])


def p_command_write(p):
    '''command	: WRITE value SEMICOLON '''
    p[0] = load_value(p[2], "b", str(p.lineno(1))) + 'PUT b\n'


def p_command_read(p):
    '''command	: READ identifier SEMICOLON '''
    initialized.add(p[2][1])
    print(variables)
    p[0] = load_addr(p[2], str(p.lineno(1))) + "GET b\n" + "LOAD a b\n"


##################################################################
####################### expression ###############################
##################################################################

def p_expression_value(p):
    '''expression   : value'''
    p[0] = load_value(p[1], "a", str(p.lineno(1)))


##################################################################
########################### value ################################
##################################################################

def p_value_num(p):
    '''value    : NUM '''
    print('value')
    p[0] = ("num", p[1])


def p_value_identifier(p):
    '''value    : identifier '''
    print('value')
    p[0] = (p[1])


##################################################################
####################### identifier ###############################
##################################################################

def p_identifier_id(p):
    '''identifier	: ID '''
    print('identifier')
    p[0] = ("id", p[1])


def p_identifier_table_id(p):
    '''identifier   : ID LBR ID RBR '''
    print('identifier')
    p[0] = ("tab", p[1], ("id", p[3]))


def p_identifier(p):
    '''identifier	: ID LBR NUM RBR '''
    print('identifier')
    p[0] = ("tab", p[1], ("num", p[3]))


def p_error(p):
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    raise Exception('Syntax error in input! Parser State:{} {} . {}'
                    .format(parser.state,
                            stack_state_str,
                            p))


parser = ply.yacc.yacc()


def test_compiler(f1='../test', f2='result.mr'):
    f = open(f1, "r")
    parsed = parser.parse(f.read(), tracking=True)
    fw = open(f2, "w")
    print(clarify(parsed))
    fw.write(clarify(parsed))
    fw.close()
    os.system('../virtual_machine/maszyna-wirtualna result.mr')


test_compiler()
