import ply.yacc
import re
from src.Exceptions import *
from src.lexer import lexer, tokens

memory_counter = 1
arrays = dict()
variables = dict()

labels_val = []


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


def is_var_taken(id, line_no):
    """ Check if id is taken."""
    if id in variables.keys():
        raise TakenVariableNameException(var=id, line_no=line_no)


def is_var_declared(id, line_no):
    """ Check if variable were declared before use."""
    if id not in variables.keys():
        raise VariableNotDeclaredException(var=id, line_no=line_no)


def check_indexes_array(idx1, idx2, line_no, id):
    """ Check if array indexes are valid."""
    if idx1 > idx2:
        raise IndexError('Error in line {}. Array {} indexes are wrong. ({}:{})'.format(line_no, id, idx1, idx2))


def add_arr(id, idx1, idx2, line_no):
    """ Save arr by id in memory and increase memory counter by array length."""
    check_indexes_array(idx1, idx2, line_no, id)
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


def begin(string: str) -> str:
    return "BEGIN {} \n".format(string)


def end(string: str) -> str:
    return "END {} \n".format(string)


def remove_labels(program):
    print(program)
    line_num = 0
    removed_labels = []
    for line in program.split("\n"):
        match = re.search("#L[0-9]+#", line)
        if match is not None:
            label_id = int(match.group()[2:-1])
            labels_val[label_id] = line_num
            line = re.sub("#L[0-9]+#", "", line)
        removed_labels.append(line)
        line_num += 1

    removed_jumps = ""
    for line in removed_labels:
        match = re.search("#J[0-9]+#", line)
        if match is not None:
            jump_id = int(match.group()[2:-1])
            jump_line = labels_val[jump_id]
            line = re.sub("#J[0-9]+#", str(jump_line), line)
        removed_jumps += line + "\n"
    return removed_jumps


##################################################################
########################### program ##############################
##################################################################
"""def p_program_declare(p):
    '''program  : DECLARE declarations BEGIN commands END'''
    p[0] = remove_labels(p[4] + "HALT")


def p_program_(p):
    '''program  : BEGIN commands END'''
    p[0] = remove_labels(p[2] + "HALT")"""


def p_program_(p):
    '''program  : BEGIN declarations END'''
    print('program')
    print(variables)
    p[0] = " HALT"
    print(variables)


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
"""def p_commands_multiple(p):
    '''commands : commands command'''
    p[0] = p[1] + p[2]


def p_commands_single(p):
    '''commands : command'''
    p[0] = p[1]"""

##################################################################
######################### command ################################
##################################################################


##################################################################
####################### expression ###############################
##################################################################

"""def p_expression_value(p):
    '''expression   : value'''
    p[0] = ("num", p[1])"""


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
    parsed = parser.parse(f.read(), tracking=True, debug=1)
    print(parsed)
    fw = open(f2, "w")
    fw.write(parsed)


test_compiler()
