import os
import sys
import numpy
import ply.yacc
from lexer import tokens
from termcolor import colored
from errors_handling.exceptions import *
from beautify import *

########################################################################################################################
############################ flags ################################################ flags ##############################
########################################################################################################################
warnings = False

########################################################################################################################
############################ memory ############################################### memory #############################
########################################################################################################################

memory_counter = 1
arrays = dict()
variables = dict()
initialized = set()
frogs = dict()
iterators = set()


########################################################################################################################
########################### getters ############################################# getters ##############################
########################################################################################################################

def get_initialized():
    return initialized


def get_arrays():
    return arrays


def get_memory_counter():
    return memory_counter


def get_variables():
    return variables


def get_iterators():
    return iterators


def spawn_frogs_multiple(n):
    """ Generate multiple labels. """
    return tuple(spawn_frog(frogs) for _ in numpy.arange(n))


########################################################################################################################
########################## setters ############################################### setters #############################
########################################################################################################################

def declare_variable(id_name, line):
    """ Save variable by id in memory and increase memory counter by 1."""
    inc_memory_counter()
    is_var_taken(id_name, line)
    variables[id_name] = get_memory_counter()


def declare_iterator(id_name, line):
    """ Save iterator by id in memory and increase memory counter by 2."""
    inc_memory_counter()
    is_var_taken(id_name, line)
    variables[id_name] = get_memory_counter()
    inc_memory_counter()


def declare_array(id_name, idx1, idx2, line):
    """ Save arr by id in memory and increase memory counter by array length."""
    validate_indexes_array(idx1, idx2, line, id_name)
    global memory_counter
    arrays[id_name] = (memory_counter + 1, idx1, idx2)
    inc_memory_counter(idx2 - idx1 + 1)


def dec_memory_counter(val=1):
    """Decrease memory counter by val(default=1)."""
    global memory_counter
    memory_counter -= val


def inc_memory_counter(val=1):
    """Increase memory counter by val(default=1)."""
    global memory_counter
    memory_counter += val


def add_iterator(it, line):
    """ Insert iterator to compiler memory, initializes  it and performs *fake declaration* """
    global iterators
    declare_iterator(it, line)
    iterators.add(it)
    initialized.add(it)


def remove_iterator(it):
    """ Removes iterator from compiler memory."""
    initialized.remove(it)
    del variables[it]


########################################################################################################################
########################## ERRORS ############################################# EXCEPTIONS #############################
########################################################################################################################

def is_initialized(id_name, line):
    """ Check if variable was initialized."""
    if id_name not in get_initialized():
        raise VariableNotInitializedException(var=id_name, line=line)


def validate_var_addr(id_name, line):
    """ Check  if var was properly used and declared."""
    if id_name not in get_variables().keys():
        if id_name in get_arrays():
            raise TypeError('Error in line {}. Wrong usage of table variable {}.'.format(id_name, line))
        else:
            raise VariableNotDeclaredException(id_name, line)


def is_var_taken(id_name, line):
    """ Check if id is taken."""
    if id_name in get_variables().keys():
        raise TakenVariableNameException(var=id_name, line=line)


def is_var_declared(id_name, line):
    """ Check if variable were declared before use."""
    if id_name not in get_variables().keys():
        raise VariableNotDeclaredException(var=id_name, line=line)


def validate_indexes_array(idx1, idx2, line, id_name):
    """ Check if array indexes are valid."""
    if idx1 > idx2:
        raise IndexError('Error in line {}. Array {} indexes are wrong. ({}:{})'.format(line, id_name, idx1, idx2))


def validate_arr(id_name, lineno):
    """ Check if use of id is valid. Array or id reference correction."""
    if id_name not in arrays:
        if id_name in variables:
            raise WrongVariableUsageException(id_name, lineno)
        else:
            raise WrongVariableUsageException(
                message="Error in line {}. Incorrect use of {} array variable.".format(lineno, id_name))


def check_var_id_arr(id_name, lineno):
    """ Check if user is not trying to get value of id variable ."""
    if id_name in arrays:
        raise WrongVariableUsageException(
            message="Error in line {}. Incorrect use of {} array variable.".format(lineno, id_name))


def check_array_num_index(variable, line):
    """ Check if usage of an array is inside it's range( indexes)"""
    mem_c, id0, id1 = arrays[variable[1]]
    if variable[2][0] == 'num' and (id0 > variable[2][1] or variable[2][1] > id1):
        raise IndexError('Line {} error. Array {} index out of interval {} used.'.format(line, variable[1], (id0, id1)))
    if variable[2][0] == 'id' and warnings:
        print(colored('[WARNING] Dynamic usage of array {}.'
                      ' Theres no way to validate index '
                      '{} correctness on python side.'.format(variable[1], variable[2][1]), 'yellow'))


def is_declared(variable, line):
    """ Check if variable has been declared."""
    if variable[0] == 'arr':
        is_declared(variable[2], line)
    elif variable[0] == 'id':
        if variable[1] not in variables.keys():
            raise VariableNotDeclaredException(var=variable[1], line=line)


def check_iterator(variable, line):
    """ Validate if there is no try to assign value to iterator."""
    if variable[1] in get_iterators():
        raise IteratorAssignException(variable, line)


def check_iterator_limit(it, lim, line):
    """ Control if user is not trying to iterate over not declared iterator. """
    if lim[0] == 'arr':
        check_iterator_limit(it, lim[2], line)
    elif lim[0] == 'id':
        if it[1] == lim[1]:
            raise IteratorLimitException(it, lim, line)


########################################################################################################################
########################## RENDERING ########################################### RENDERING #############################
########################################################################################################################
def cmd(command, *r):
    """Generates commands by input command + registers."""
    brackets = len(r) * '{} '
    return command.upper() + " " + brackets[:-1].format(*r) + '\n'


def generate_number(number, reg):
    """ Function generate number in register. """
    commands = ""
    while number != 0:
        if number % 2 == 0:
            number = number // 2
            commands = concat("SHL", reg, nl(), commands)
        else:
            number -= 1
            commands = concat("INC", reg, nl(), commands)
    commands = concat(cmd('reset', reg), commands)
    return commands


def get_addr(variable, reg, line, r_opt='c'):
    """ Function is responsible for generating memory address of given variable"""
    if variable[0] == 'id':
        check_var_id_arr(variable[1], line)  # err 12
        is_declared(variable, line)
        return pack(generate_number(variables[variable[1]], reg), '<<id_addr>>')
    elif variable[0] == 'arr':
        validate_arr(variable[1], line)
        mem, id1, id2 = arrays[variable[1]]
        check_array_num_index(variable, line)
        n1 = get_value(variable[2], reg, line)
        n2 = generate_number(id1, r_opt)
        n3 = generate_number(mem, r_opt)
        return pack(n1 + n2 + cmd('sub', reg, r_opt) + n3 + cmd('add', reg, r_opt), '<<arr_addr>>')
    elif variable[0] == 'num':
        raise Exception('You are trying to find an address of a number. {}'.format(variable))
    else:
        raise Exception('Unknown type of {}. It is neither array nor id nor num.'.format(variable))


def get_value(variable, reg, line, r_opt='c'):
    """ Function is responsible for direct value generation. """
    if variable[0] == 'num':
        return pack(generate_number(variable[1], reg), '<<num_value_gen>>')
    elif variable[0] == 'id':
        check_var_id_arr(variable[1], line)  # err 12
        is_declared(variable, line)
        is_initialized(variable[1], line)
        return pack(get_addr(variable, reg, line) + cmd('load', reg, reg), '<<id_value_gen>>')
    elif variable[0] == 'arr':
        return pack(get_addr(variable, reg, line, r_opt) + cmd('load', reg, reg), '<<arr_value_gen>>')
    else:
        raise Exception('Unknown type of {}. It is neither array nor id nor num.'.format(variable))


########################################################################################################################
########################### program ############################################# program ##############################
########################################################################################################################

def p_program_declare(p):
    """program  : DECLARE declarations BEGIN commands END"""
    p[0] = p[4] + "HALT"


def p_program_(p):
    """program  : BEGIN commands END"""
    p[0] = + p[2] + "HALT"


########################################################################################################################
###################### declarations ######################################## declarations ##############################
########################################################################################################################

def p_declarations_variable_rec(p):
    """declarations : declarations COMMA ID"""
    declare_variable(p[3], p.lineno(3))


def p_declarations_array_rec(p):
    """declarations : declarations COMMA ID LBR NUM COLON NUM RBR"""
    declare_array(p[3], p[5], p[7], str(p.lineno(3)))


def p_declarations_variable(p):
    """declarations : ID"""
    declare_variable(p[1], p.lineno(1))


def p_declarations_array(p):
    """declarations : ID LBR NUM COLON NUM RBR"""
    declare_array(p[1], p[3], p[5], str(p.lineno(1)))


########################################################################################################################
######################## commands ############################################ commands ################################
########################################################################################################################
def p_commands_multiple(p):
    """commands : commands command"""
    p[0] = p[1] + p[2]


def p_commands_single(p):
    """commands : command"""
    p[0] = p[1]


########################################################################################################################
####################### command ################################################# command ##############################
########################################################################################################################
def p_command_assign(p):
    """command  : identifier ASSIGN expression SEMICOLON"""
    check_iterator(p[1], p.lineno(1))
    p[0] = pack(p[3]
                + get_addr(p[1], 'b', p.lineno(1))
                + cmd('store', 'a', 'b'), '<<asg>>')
    initialized.add(p[1][1])


def p_command_read(p):
    """command	: READ identifier SEMICOLON """
    initialized.add(p[2][1])
    is_declared(p[2], p.lineno(2))
    p[0] = pack(get_addr(p[2], "b", p.lineno(2))
                + cmd('get', 'b'), '<<read>>')


def p_command_write(p):
    """command	: WRITE value SEMICOLON """
    if p[2][0] == 'num':
        content = generate_number(p[2][1], 'c') + cmd('reset', 'b') + cmd('store', 'c', 'b')
    else:
        is_initialized(p[2][1], p.lineno(2))
        content = get_addr(p[2], "b", p.lineno(2))
    p[0] = pack(content
                + cmd('put', 'b'), '<<write>>')


def p_command_if(p):
    """command	: IF condition THEN commands ENDIF"""
    p[0] = pack(p[2][0] +
                p[4] +
                p[2][1], '<<if>>')


def p_command_if_else(p):
    """command	: IF condition THEN commands ELSE commands ENDIF"""
    m1 = spawn_frog(frogs)
    p[0] = pack(p[2][0] +
                p[4] +
                cmd('jump', frogs[m1]) +
                p[2][1] + p[6] + m1, '<<if_else>>')


def p_command_while(p):
    """command	: WHILE condition DO commands ENDWHILE"""
    m1 = spawn_frog(frogs)
    p[0] = pack(m1 +
                p[2][0] +
                p[4] +
                cmd('jump', frogs[m1]) +
                p[2][1], '<<while>>')


def p_command_repeat_until(p):
    """command	: REPEAT commands UNTIL condition SEMICOLON"""
    p[0] = pack(p[4][1] +
                p[2] +
                p[4][0], '<<repeat_until>>')


def p_command_for_to(p):
    """command  : FOR iterator FROM value TO value DO commands ENDFOR"""
    check_iterator_limit(p[2], p[4], p.lineno(4))
    check_iterator_limit(p[2], p[6], p.lineno(6))
    v1 = get_value(p[4], 'e', p.lineno(4), 'f')
    v2 = get_value(p[6], 'f', p.lineno(6), 'd')
    it_addr = get_addr(p[2], 'c', p.lineno(2), 'd')
    m1, m2, m3 = spawn_frogs_multiple(3)
    p[0] = pack(v1 + it_addr +
                cmd('store', 'e', 'c') +
                cmd('inc', 'c') +
                v2 +
                cmd('store', 'f', 'c') +
                m2 + it_addr +
                cmd('inc', 'c') +
                cmd('load', 'f', 'c') +
                cmd('sub', 'e', 'f') +
                cmd('jzero', 'e', frogs[m3]) +
                cmd('jump', frogs[m1]) +
                m3 + p[8] +
                it_addr +
                cmd('load', 'e', 'c') +
                cmd('inc', 'e') +
                cmd('store', 'e', 'c') +
                cmd('jump', frogs[m2]) +
                m1, '<<for_to>>')
    remove_iterator(p[2][1])


def p_command_for_downto(p):
    """command  : FOR iterator FROM value DOWNTO value DO commands ENDFOR"""
    check_iterator_limit(p[2], p[4], p.lineno(4))
    check_iterator_limit(p[2], p[6], p.lineno(6))
    v1 = get_value(p[4], 'e', p.lineno(4), 'f')  # BIGGER
    v2 = get_value(p[6], 'f', p.lineno(6), 'd')
    it_addr = get_addr(p[2], 'c', p.lineno(2), 'd')
    m1, m2, m3 = spawn_frogs_multiple(3)
    p[0] = pack(v1 + it_addr +
                cmd('store', 'e', 'c') +
                cmd('inc', 'c') +
                v2 +
                cmd('reset', 'd') +
                cmd('add', 'd', 'f') +
                cmd('sub', 'd', 'e') +
                cmd('jzero', 'd', frogs[m3]) +
                cmd('jump', frogs[m1]) +
                m3 + cmd('reset', 'd') +
                cmd('add', 'd', 'e') +
                cmd('sub', 'd', 'f') +
                cmd('inc', 'd') +
                cmd('store', 'd', 'c') +
                m2 + it_addr +
                cmd('inc', 'c') +
                cmd('load', 'd', 'c') +
                cmd('jzero', 'd', frogs[m1]) +
                p[8] +
                it_addr +
                cmd('load', 'e', 'c') +
                cmd('dec', 'e') +
                cmd('store', 'e', 'c') +
                cmd('inc', 'c') +
                cmd('load', 'e', 'c') +
                cmd('dec', 'e') +
                cmd('store', 'e', 'c') +
                cmd('jump', frogs[m2]) +
                m1, '<<for_downto>>')
    remove_iterator(p[2][1])


def p_iterator(p):
    """iterator	: ID """
    p[0] = ('id', p[1])
    add_iterator(p[1], p.lineno(1))


########################################################################################################################
####################### expression ################################################# expression ########################
########################################################################################################################

def p_expression_value(p):
    """expression   : value"""
    p[0] = pack(get_value(p[1], "a", str(p.lineno(1))),
                "<<expr_value>>")


def p_expression_plus(p):
    """expression   : value PLUS value"""
    v1 = get_value(p[1], 'a', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    p[0] = pack(v1 + v2 +
                cmd('add', 'a', 'c'),
                '<<plus>>')


def p_expression_minus(p):
    """expression   : value MINUS value"""
    v1 = get_value(p[1], 'a', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    p[0] = pack(v1 + v2 +
                cmd('sub', 'a', 'c'),
                '<<plus>>')


def p_expression_multiplication(p):
    """expression   : value MULT value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2, m3, m4, m5 = spawn_frogs_multiple(5)
    p[0] = pack(v1 + v2
                + cmd('reset', 'a')
                + cmd('add', 'a', 'd')
                + cmd('sub', 'a', 'c')
                + cmd('jzero', 'a', frogs[m5])
                + get_value(p[3], 'd', p.lineno(3), 'c')
                + get_value(p[1], 'c', p.lineno(1), 'b')
                + m5
                + cmd('reset', 'a')
                + cmd('jzero', 'c', frogs[m2])
                + m4 + cmd('jzero', 'd', frogs[m2])
                + cmd('jodd', 'd', frogs[m3])
                + cmd('jump', frogs[m1])
                + m3 + cmd('add', 'a', 'c')
                + m1 + cmd('shr', 'd')
                + cmd('shl', 'c')
                + cmd('jump', frogs[m4])
                + m2, '<<mult>>')


"""unsigned int    p[0] = pack(v1 + v2
                + cmd('reset', 'a')
                + cmd('jzero', 'c', frogs[m2])
                + m3 + cmd('jzero', 'd', frogs[m2])
                + cmd('jodd', 'd', frogs[m1])
                + cmd('shl', 'c')
                + cmd('shr', 'd')
                + m1 + cmd('add', 'a', 'c')
                + cmd('dec', 'd')
                + cmd('jump', frogs[m3])
                + m2,
                '<<mult>>')"""


def p_expression_division(p):
    """expression   : value DIV value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2, m3, m4, m5, m6 = spawn_frogs_multiple(6)
    p[0] = pack(v1 + v2 +
                cmd('reset', 'a') +
                cmd('jzero', 'c', frogs[m1]) +
                cmd('jzero', 'd', frogs[m1]) +
                cmd('reset', 'e') +
                cmd('reset', 'f') +
                cmd('reset', 'b') +
                cmd('add', 'b', 'c') +
                m3 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'd') +
                cmd('jzero', 'e', frogs[m5]) +
                cmd('jump', frogs[m1]) +
                m5 + cmd('reset', 'f') +
                cmd('inc', 'f') +
                cmd('shl', 'c') +
                m4 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'd') +
                cmd('jzero', 'e', frogs[m6]) +
                cmd('jump', frogs[m2]) +
                m6 + cmd('shl', 'f') +
                cmd('shl', 'c') +
                cmd('jump', frogs[m4]) +
                m2 + cmd('add', 'a', 'f') +
                cmd('reset', 'f') +
                cmd('shr', 'c') +
                cmd('sub', 'd', 'c') +
                cmd('reset', 'c') +
                cmd('add', 'c', 'b') +
                cmd('jump', frogs[m3]) +
                m1,
                '<<div>>')


def p_expression_modulo(p):
    """expression   : value MOD value"""
    v1 = get_value(p[1], 'a', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2, m3, m4, m5, m6, m7 = spawn_frogs_multiple(7)
    p[0] = pack(v1 + v2 +
                cmd('reset', 'd') +
                cmd('jzero', 'c', frogs[m7]) +
                cmd('jzero', 'a', frogs[m7]) +
                cmd('reset', 'e') +
                cmd('reset', 'f') +
                cmd('reset', 'b') +
                cmd('add', 'b', 'c') +
                m3 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'a') +
                cmd('jzero', 'e', frogs[m5]) +
                cmd('jump', frogs[m1]) +
                m5 + cmd('reset', 'f') +
                cmd('inc', 'f') +
                cmd('shl', 'c') +
                m4 + cmd('reset', 'e') +
                cmd('add', 'e', 'c') +
                cmd('sub', 'e', 'a') +
                cmd('jzero', 'e', frogs[m6]) +
                cmd('jump', frogs[m2]) +
                m6 + cmd('shl', 'f') +
                cmd('shl', 'c') +
                cmd('jump', frogs[m4]) +
                m2 + cmd('add', 'd', 'f') +
                cmd('reset', 'f') +
                cmd('shr', 'c') +
                cmd('sub', 'a', 'c') +
                cmd('reset', 'c') +
                cmd('add', 'c', 'b') +
                cmd('jump', frogs[m3]) +
                m7 + cmd('reset', 'a') +
                m1,
                '<<mod>>')


########################################################################################################################
######################## condition ####################################################### condition ###################
########################################################################################################################
def p_condition_gt(p):
    """condition   : value GT value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1 = spawn_frog(frogs)
    p[0] = (pack(v1 + v2
                 + cmd('sub', 'c', 'd')
                 + cmd('jzero', 'c', frogs[m1]), '<<gt>>'), m1)


def p_condition_lt(p):
    """condition   : value LT value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1 = spawn_frog(frogs)
    p[0] = (pack(v1 + v2
                 + cmd('sub', 'c', 'd')
                 + cmd('jzero', 'c', frogs[m1]), '<<lt>>'), m1)


def p_condition_geq(p):
    """condition   : value GEQ value"""
    v1 = get_value(p[1], 'd', p.lineno(1), 'c')
    v2 = get_value(p[3], 'c', p.lineno(3), 'b')
    m1, m2 = spawn_frogs_multiple(2)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('sub', 'e', 'd') +
                 cmd('jzero', 'e', frogs[m1]) +
                 cmd('jump', frogs[m2]) +
                 m1,
                 '<<geq>>'), m2)


def p_condition_leq(p):
    """condition   : value LEQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2 = spawn_frogs_multiple(2)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('sub', 'e', 'd') +
                 cmd('jzero', 'e', frogs[m1]) +
                 cmd('jump', frogs[m2]) +
                 m1,
                 '<<leq>>'), m2)


def p_condition_eq(p):
    """condition   : value EQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2, m3 = spawn_frogs_multiple(3)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('reset', 'f') +
                 cmd('add', 'f', 'd') +
                 cmd('sub', 'e', 'd') +
                 cmd('sub', 'f', 'c') +
                 cmd('jzero', 'e', frogs[m3]) +
                 cmd('jump', frogs[m2]) +
                 m3 + cmd('jzero', 'f', frogs[m1]) +
                 cmd('jump', frogs[m2]) +
                 m1,
                 '<<eq>>'), m2)


def p_condition_neq(p):
    """condition   : value NEQ value"""
    v1 = get_value(p[1], 'c', p.lineno(1), 'd')
    v2 = get_value(p[3], 'd', p.lineno(3), 'b')
    m1, m2, m3 = spawn_frogs_multiple(3)
    p[0] = (pack(v1 + v2 +
                 cmd('reset', 'e') +
                 cmd('add', 'e', 'c') +
                 cmd('reset', 'f') +
                 cmd('add', 'f', 'd') +
                 cmd('sub', 'e', 'd') +
                 cmd('sub', 'f', 'c') +
                 cmd('jzero', 'e', frogs[m3]) +
                 cmd('jump', frogs[m1]) +
                 m3 + cmd('jzero', 'f', frogs[m2]) +
                 cmd('jump', frogs[m1]) +
                 m1,
                 '<<neq>>'), m2)


########################################################################################################################
########################### value ############################################### value ################################
########################################################################################################################

def p_value_num(p):
    """value    : NUM """
    p[0] = ("num", p[1])


def p_value_identifier(p):
    """value    : identifier """
    p[0] = (p[1])


########################################################################################################################
######################### identifier ######################################### identifier ##############################
########################################################################################################################

def p_identifier_id(p):
    """identifier	: ID """
    p[0] = ("id", p[1])


def p_identifier_table_recursive(p):
    """identifier   : ID LBR ID RBR """
    p[0] = ("arr", p[1], ("id", p[3]))


def p_identifier_table_element(p):
    """identifier	: ID LBR NUM RBR """
    p[0] = ("arr", p[1], ("num", p[3]))


def p_error(p):
    raise SyntaxError('Error in line {}. Syntax error in {}'.format(p.lineno, p))


parser = ply.yacc.yacc()


def main(args):
    if len(args) < 2:
        p1 = 'Arguments input error: {} .You need to input exactly two arguments!.'.format(args)
        raise Exception(colored(p1 + '\n Example usage python3 kompilator.py file_in file_out \n ', 'red'))
    if len(args) == 3 and args[2] == '--warnings':
        global warnings
        warnings = True
    with open(args[0], "r") as f:
        with open(args[1], "w+") as f_out:
            parsed = parser.parse(f.read(), tracking=False)
            clear = unpack(parsed)
            no_labels = kill_frogs(clear, frogs)
            f_out.write(no_labels)
    if len(args) == 3:
        if args[2] == '--vm' or args[2] == '-vm':
            os.system('virtual_machine/maszyna-wirtualna-cln ' + args[1])


main(sys.argv[1:])
