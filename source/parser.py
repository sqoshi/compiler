import os
import numpy
from termcolor import colored
from errors_handling.exceptions import *
from lexer import tokens
import ply.yacc

from beautify import *

memory_counter = 1
arrays = dict()
variables = dict()
initialized = set()
jump_label = dict()
iterators_set = set()


########################################################################################################################
########################### control ############################################# control ##############################
########################################################################################################################

def add_var(id, line):
    """ Save variable by id in memory and increase memory counter by 1."""
    inc_memory_counter()
    is_var_taken(id, line)
    variables[id] = get_memory_counter()


def get_initialized():
    return initialized


def get_arrays():
    return arrays


def get_memory_counter():
    return memory_counter


def get_variables():
    return variables


def dec_memory_counter(val=1):
    """Decrease memory counter by val(default=1)."""
    global memory_counter
    memory_counter -= val


def inc_memory_counter(val=1):
    """Increase memory counter by val(default=1)."""
    global memory_counter
    memory_counter += val


def add_iterator(it, line):
    global iterators_set
    add_var(it, line)
    iterators_set.add(it)
    initialized.add(it)


def remove_iterator(it):
    initialized.remove(it)
    del variables[it]


def get_iterators():
    return iterators_set


def is_initialized(id, line):
    """ Check if variable was initialized."""
    if id not in get_initialized():
        raise VariableNotInitializedException(var=id, line=line)


def validate_var_addr(id, line):
    """ Check  if var was properly used and declared."""
    if id not in get_variables().keys():
        if id in get_arrays():
            raise TypeError('Error in line {}. Wrong usage of table variable {}.'.format(id, line))
        else:
            raise VariableNotDeclaredException(id, line)


def is_var_taken(id, line):
    """ Check if id is taken."""
    if id in get_variables().keys():
        raise TakenVariableNameException(var=id, line=line)


def is_var_declared(id, line):
    """ Check if variable were declared before use."""
    if id not in get_variables().keys():
        raise VariableNotDeclaredException(var=id, line=line)


def validate_indexes_array(idx1, idx2, line, id):
    """ Check if array indexes are valid."""
    if idx1 > idx2:
        raise IndexError('Error in line {}. Array {} indexes are wrong. ({}:{})'.format(line, id, idx1, idx2))


def add_arr(id, idx1, idx2, line):
    """ Save arr by id in memory and increase memory counter by array length."""
    validate_indexes_array(idx1, idx2, line, id)
    global memory_counter
    arrays[id] = (memory_counter + 1, idx1, idx2)
    inc_memory_counter(idx2 - idx1 + 1)


def validate_arr(id, lineno):
    if id not in arrays:
        if id in variables:
            raise Exception("Error in line {}. Incorrect use of {} variable.".format(lineno, id) + id)
        else:
            raise Exception("Error in line {}. Incorrect use of {} array variable.".format(lineno, id) + id)


def get_marks(n):
    """ Generate multiple labels. """
    return tuple(mark(jump_label) for _ in numpy.arange(n))


def check_array_num_index(variable, line):
    mem_c, id0, id1 = arrays[variable[1]]
    if variable[2][0] == 'num' and (id0 > variable[2][1] or variable[2][1] > id1):
        raise IndexError('Line {} error. Array {} index out of interval {} used.'.format(line, variable[1], (id0, id1)))
    if variable[2][0] == 'id':
        print(colored(
            '[WARNING] Dynamic usage of array {}. Theres no way to validate index {} correctness on python side.'.format(
                variable[1], variable[2][1]), 'red'))


########################################################################################################################
########################## RENDERING ########################################### RENDERING #############################
########################################################################################################################
def cmd(command, *r):
    brackets = len(r) * '{} '
    return command.upper() + " " + brackets[:-1].format(*r) + '\n'


def rs_reg(reg):
    return 'RESET ' + str(reg) + nl()


def generate_number(number, reg):
    commands = ""
    while number != 0:
        if number % 2 == 0:
            number = number // 2
            commands = concat("SHL", reg, nl(), commands)
        else:
            number -= 1
            commands = concat("INC", reg, nl(), commands)
    commands = concat(rs_reg(reg), commands)
    return commands


def get_addr(variable, reg, line, r_opt='c'):
    if variable[0] == 'id':
        return generate_number(variables[variable[1]], reg)
    elif variable[0] == 'arr':
        validate_arr(variable[1], line)
        mem, id1, id2 = arrays[variable[1]]
        check_array_num_index(variable, line)
        # blad z generowaniem tabllicy np jesli na 9 komorce jest w pamieci, a ind 4 to start
        return get_value(variable[2], reg, line) + generate_number(id1, r_opt) + cmd('sub', reg, r_opt) \
               + generate_number(id1, r_opt) + cmd('add', reg, r_opt)
    elif variable[0] == 'num':
        raise Exception('You are trying to find an address of a number. {}'.format(variable))
    else:
        raise Exception('Unknown type of {}. It is neither array nor id nor num.'.format(variable))


def get_value(variable, reg, line, r_opt='c'):
    if variable[0] == 'num':
        return generate_number(variable[1], reg)
    elif variable[0] == 'id':
        is_var_declared(variable[1], line)
        is_initialized(variable[1], line)
        return get_addr(variable, reg, line) + cmd('load', reg, reg)
    elif variable[0] == 'arr':
        return get_addr(variable, reg, line, r_opt) + cmd('load', reg, reg)
    else:
        raise Exception('Unknown type of {}. It is neither array nor id nor num.'.format(variable))


########################################################################################################################
########################### program ############################################# program ##############################
########################################################################################################################

def p_program_declare(p):
    """program  : DECLARE declarations BEGIN commands END"""
    print(variables)
    print(arrays)
    p[0] = p[4] + "HALT"


def p_program_(p):
    """program  : BEGIN commands END"""
    print(variables)
    print(arrays)
    p[0] = + p[2] + "HALT"


##################################################################
###################### declarations ##############################
##################################################################

def p_declarations_variable_rec(p):
    """declarations : declarations COMMA ID"""
    id, line = p[3], str(p.lineno(3))
    add_var(id, line)


def p_declarations_array_rec(p):
    """declarations : declarations COMMA ID LBR NUM COLON NUM RBR"""
    add_arr(p[3], p[5], p[7], str(p.lineno(3)))


def p_declarations_variable(p):
    """declarations : ID"""
    id, line = p[1], str(p.lineno(1))
    add_var(id, line)


def p_declarations_array(p):
    """declarations : ID LBR NUM COLON NUM RBR"""
    add_arr(p[1], p[3], p[5], str(p.lineno(1)))


##################################################################
######################## commands ################################
##################################################################
def p_commands_multiple(p):
    """commands : commands command"""
    p[0] = p[1] + p[2]


def p_commands_single(p):
    """commands : command"""
    p[0] = p[1]


##################################################################
######################### command ################################
##################################################################
def p_command_assign(p):
    """command  : identifier ASSIGN expression SEMICOLON"""
    identifier, expression, line = p[1], p[3], str(p.lineno(1))
    p[0] = pack(str(expression) + get_addr(identifier, 'b', line) + cmd('store', 'a', 'b'), '<<asg>>')
    initialized.add(identifier[1])


def p_command_read(p):
    """command	: READ identifier SEMICOLON """
    initialized.add(p[2][1])
    p[0] = pack(get_addr(p[2], "b", str(p.lineno(1))) + cmd('get', 'b'), '<<read>>')


def p_command_write(p):
    """command	: WRITE identifier SEMICOLON """
    p[0] = pack(get_addr(p[2], "b", str(p.lineno(1))) + cmd('put', 'b'), '<<write>>')


def p_command_if(p):
    """command	: IF condition THEN commands ENDIF"""
    p[0] = pack(p[2][0] +
                p[4] +
                p[2][1], '<<if>>')


def p_command_if_else(p):
    """command	: IF condition THEN commands ELSE commands ENDIF"""
    m1 = mark(jump_label)
    p[0] = pack(p[2][0] +
                p[4] +
                cmd('jump', jump_label[m1]) +
                p[2][1] + p[6] + m1, '<<if_else>>')


def p_command_while(p):
    """command	: WHILE condition DO commands ENDWHILE"""
    m1 = mark(jump_label)
    p[0] = pack(m1
                + p[2][0]
                + p[4]
                + cmd('jump', jump_label[m1])
                + p[2][1], '<<while>>')


def p_command_repeat_until(p):
    """command	: REPEAT commands UNTIL condition SEMICOLON"""
    m1 = mark(jump_label)
    p[0] = pack(
        m1 + p[2]
        + p[4][0]
        + cmd('jump', jump_label[m1])
        + p[4][1], '<<repeat_until>>')


##################################################################
####################### expression ###############################
##################################################################

def p_expression_value(p):
    """expression   : value"""
    p[0] = pack(get_value(p[1], "a", str(p.lineno(1))), "<<expr_value>>")


def p_expression_plus(p):
    """expression   : value PLUS value"""
    v1 = get_value(p[1], 'a', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    p[0] = pack(v1 + v2 + cmd('add', 'a', 'c') + nl(), '<<plus>>')


def p_expression_minus(p):
    """expression   : value MINUS value"""
    v1 = get_value(p[1], 'a', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    p[0] = pack(v1 + v2 + cmd('sub', 'a', 'c') + nl(), '<<plus>>')


def p_expression_multiplication(p):
    """expression   : value MULT value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2, m3 = get_marks(3)
    p[0] = pack(v1 + v2 +
                cmd('reset', 'a')
                + m3 + cmd('jzero', 'd', jump_label[m2])
                + cmd('jodd', 'd', jump_label[m1])
                + cmd('shl', 'c')
                + cmd('shr', 'd')
                + m1 + cmd('add', 'a', 'c')
                + cmd('dec', 'd')
                + cmd('jump', jump_label[m3])
                + m2,
                '<<mult>>')


def p_expression_division(p):
    """expression   : value DIV value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2, m3, m4, m5, m6 = get_marks(6)
    p[0] = pack(v1 + v2 +
                cmd('reset', 'a') +
                cmd('jzero', 'c', jump_label[m1]) +
                cmd('jzero', 'd', jump_label[m1]) +
                cmd('reset', 'e') +
                cmd('reset', 'f') +
                cmd('reset', 'b') +
                cmd('add', 'b', 'c') +
                m3 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'd') +
                cmd('jzero', 'e', jump_label[m5]) +
                cmd('jump', jump_label[m1]) +
                m5 + cmd('reset', 'f') +
                cmd('inc', 'f') +
                cmd('shl', 'c') +
                m4 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'd') +
                cmd('jzero', 'e', jump_label[m6]) +
                cmd('jump', jump_label[m2]) +
                m6 + cmd('shl', 'f') +
                cmd('shl', 'c') +
                cmd('jump', jump_label[m4]) +
                m2 + cmd('add', 'a', 'f') +
                cmd('reset', 'f') +
                cmd('shr', 'c') +
                cmd('sub', 'd', 'c') +
                cmd('reset', 'c') +
                cmd('add', 'c', 'b') +
                cmd('jump', jump_label[m3]) +
                m1, '<<div>>')


def p_expression_modulo(p):
    """expression   : value MOD value"""
    v1 = get_value(p[1], 'a', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2, m3, m4, m5, m6 = get_marks(6)
    p[0] = pack(v1 + v2 +
                cmd('reset', 'd') +
                cmd('jzero', 'c', jump_label[m1]) +
                cmd('jzero', 'a', jump_label[m1]) +
                cmd('reset', 'e') +
                cmd('reset', 'f') +
                cmd('reset', 'b') +
                cmd('add', 'b', 'c') +
                m3 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'a') +
                cmd('jzero', 'e', jump_label[m5]) +
                cmd('jump', jump_label[m1]) +
                m5 + cmd('reset', 'f') +
                cmd('inc', 'f') +
                cmd('shl', 'c') +
                m4 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'a') +
                cmd('jzero', 'e', jump_label[m6]) +
                cmd('jump', jump_label[m2]) +
                m6 + cmd('shl', 'f') +
                cmd('shl', 'c') +
                cmd('jump', jump_label[m4]) +
                m2 + cmd('add', 'd', 'f') +
                cmd('reset', 'f') +
                cmd('shr', 'c') +
                cmd('sub', 'a', 'c') +
                cmd('reset', 'c') +
                cmd('add', 'c', 'b') +
                cmd('jump', jump_label[m3]) +
                m1, '<<mod>>')


##################################################################
######################## condition ###############################
##################################################################
def p_condition_gt(p):
    """condition   : value GT value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1 = mark(jump_label)
    p[0] = (pack(v1 + v2
                 + cmd('sub', 'c', 'd')
                 + cmd('jzero', 'c', jump_label[m1])
                 , '<<GT>>'), m1)


def p_condition_lt(p):
    """condition   : value LT value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1 = mark(jump_label)
    p[0] = (pack(v1 + v2
                 + cmd('sub', 'c', 'd')
                 + cmd('jzero', 'c', jump_label[m1])
                 , '<<LT>>'), m1)


def p_condition_geq(p):
    """condition   : value GEQ value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2 = get_marks(2)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('sub', 'e', 'd') +
                 cmd('jzero', 'e', jump_label[m1]) +
                 cmd('jump', jump_label[m2]) +
                 m1
                 , '<<geq>>'), m2)


def p_condition_leq(p):
    """condition   : value LEQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2 = get_marks(2)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('sub', 'e', 'd') +
                 cmd('jzero', 'e', jump_label[m1]) +
                 cmd('jump', jump_label[m2]) +
                 m1
                 , '<<leq>>'), m2)


def p_condition_eq(p):
    """condition   : value EQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2, m3 = get_marks(3)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('reset', 'f') +
                 cmd('add', 'f', 'd') +
                 cmd('sub', 'e', 'd') +
                 cmd('sub', 'f', 'c') +
                 cmd('jzero', 'e', jump_label[m3]) +
                 cmd('jump', jump_label[m2]) +
                 m3 + cmd('jzero', 'f', jump_label[m1]) +
                 cmd('jump', jump_label[m2]) +
                 m1
                 , '<<eq>>'), m2)


def p_condition_neq(p):
    """condition   : value NEQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2, m3 = get_marks(3)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('reset', 'f') +
                 cmd('add', 'f', 'd') +
                 cmd('sub', 'e', 'd') +
                 cmd('sub', 'f', 'c') +
                 cmd('jzero', 'e', jump_label[m3]) +
                 cmd('jump', jump_label[m1]) +
                 m3 + cmd('jzero', 'f', jump_label[m2]) +
                 cmd('jump', jump_label[m1]) +
                 m1
                 , '<<neq>>'), m2)


##################################################################
########################### value ################################
##################################################################

def p_value_num(p):
    '''value    : NUM '''
    p[0] = ("num", p[1])


def p_value_identifier(p):
    '''value    : identifier '''
    p[0] = (p[1])


##################################################################
####################### identifier ###############################
##################################################################

def p_identifier_id(p):
    '''identifier	: ID '''
    p[0] = ("id", p[1])


def p_identifier_table_recursive(p):
    '''identifier   : ID LBR ID RBR '''
    p[0] = ("arr", p[1], ("id", p[3]))


def p_identifier_table_element(p):
    '''identifier	: ID LBR NUM RBR '''
    p[0] = ("arr", p[1], ("num", p[3]))


def p_error(p):
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    raise Exception('Syntax error in input! Parser State:{} {} . {}'
                    .format(parser.state,
                            stack_state_str,
                            p))


parser = ply.yacc.yacc()


def test_compiler(f1='../examples/tests/my_tests/test', f2='result.mr'):
    f = open(f1, "r")
    parsed = parser.parse(f.read(), tracking=True)
    fw = open(f2, "w")
    clear = unpack(parsed)
    no_labels = remove_marks(clear, jump_label)
    fw.write(no_labels)
    fw.close()
    os.system('../virtual_machine/maszyna-wirtualna result.mr')


t0 = '../examples/tests/program0.imp'
t1 = '../examples/tests/program1.imp'
t2 = '../examples/tests/program2.imp'
test_compiler()
