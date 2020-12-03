import os
import numpy

from errors_handling.exceptions import *
from lexer import tokens
import ply.yacc

from source.beautify import *
from source.memory import *


##################################################################
########################### program ##############################
##################################################################
def p_program_declare(p):
    """program  : DECLARE declarations BEGIN commands END"""
    p[0] = p[4] + "HALT"


def p_program_(p):
    """program  : BEGIN commands END"""
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
    p[0] = pack(str(expression) + render_by_addr(identifier, line, "b") + "STORE a b" + nl(), '<<asg')
    initialized.add(identifier[1])


def p_command_write(p):
    """command	: WRITE value SEMICOLON """
    p[0] = pack(render_value(p[2], str(p.lineno(1)), "b") + 'PUT b' + nl(), '<<write')


def p_command_read(p):
    """command	: READ identifier SEMICOLON """
    initialized.add(p[2][1])
    p[0] = render_by_addr(p[2], str(p.lineno(1)), "b") + "GET b" + nl()


def p_command_while(p):
    """command	: WHILE condition DO commands ENDWHILE"""
    m1 = mark(jump_label)
    p[0] = pack(m1 + p[2][0] + p[4]
                + "JUMP " + jump_label[m1] + nl() + p[2][1], '<<while')


def p_command_repeat_until(p):
    """command	: REPEAT commands UNTIL condition SEMICOLON"""
    m1 = mark(jump_label)
    print(m1 + p[2] + nl() + p[4][0] + p[4][1] + "JUMP " + jump_label[m1] + nl())
    p[0] = pack(m1 + p[2] + nl() + p[4][0] + "JUMP " + jump_label[m1] + nl() +p[4][1], '<<repeat_until')


def p_command_if(p):
    """command	: IF condition THEN commands ENDIF"""
    p[0] = pack(p[2][0] + p[4] + nl() + p[2][1], '<<if')


def p_command_if_else(p):
    """command	: IF condition THEN commands ELSE commands ENDIF"""
    m1 = mark(jump_label)
    p[0] = pack(p[2][0] + p[4] + nl()
                + "JUMP " + jump_label[m1] + nl()
                + p[2][1] + p[6] + m1, '<<if_else')


##################################################################
####################### expression ###############################
##################################################################

def p_expression_value(p):
    """expression   : value"""
    p[0] = pack(render_value(p[1], str(p.lineno(1)), "a"), "<<valexp")


def p_expression_plus(p):
    """expression   : value PLUS value"""
    command = standard_render(p[1], p[3], 'a', 'c', str(p.lineno(2)))
    p[0] = pack(command + "ADD a c" + nl(), '<<plus')


def p_expression_minus(p):
    """expression   : value MINUS value"""
    command = standard_render(p[1], p[3], 'a', 'c', str(p.lineno(2)))
    p[0] = pack(command + "SUB a c" + nl(), '<<minus')


def p_expression_multiplication(p):
    """expression   : value MULT value"""
    command = standard_render(p[1], p[3], 'd', 'c', str(p.lineno(2)))
    m1, m2, m3 = get_marks(3)
    p[0] = pack(command
                + rs_reg('a') + nl()
                + m3 + "JZERO d " + jump_label[m2] + nl()
                + "JODD d " + jump_label[m1] + nl()
                + "SHL c" + nl() + 'SHR d' + nl()
                + m1 + "ADD a c" + nl() + "DEC d" + nl()
                + "JUMP " + jump_label[m3] + nl()
                + m2,
                '<<mult')


def p_expression_division(p):
    """expression   : value DIV value"""
    command = standard_render(p[1], p[3], 'd', 'c', str(p.lineno(2)))
    m1, m2, m3 = get_marks(3)
    p[0] = pack(command
                + m3 + rs_reg('e') + nl()
                + 'ADD e c' + nl()
                + "SUB e d" + nl()
                + 'JZERO e ' + jump_label[m1] + nl()
                + 'JUMP ' + jump_label[m2] + nl()
                + m1 + "JUMP " + jump_label[m3] + nl()
                + m2
                , '<<div')


##################################################################
######################## condition ###############################
##################################################################
def p_condition_gt(p):
    """condition   : value GT value"""
    command = standard_render(p[1], p[3], 'c', 'd', str(p.lineno(2)))
    m1 = mark(jump_label)
    p[0] = (pack(command
                 + "SUB c d" + nl()
                 + 'JZERO c ' + jump_label[m1] + nl()
                 , '<<GT'), m1)


def p_condition_lt(p):
    """condition   : value LT value"""
    command = standard_render(p[1], p[3], 'd', 'c', str(p.lineno(2)))
    m1 = mark(jump_label)
    p[0] = (pack(command
                 + "SUB c d" + nl()
                 + 'JZERO c ' + jump_label[m1] + nl()
                 , '<<LT'), m1)


def p_condition_geq(p):
    """condition   : value GEQ value"""
    command = standard_render(p[1], p[3], 'd', 'c', str(p.lineno(2)))
    m1, m2 = get_marks(2)
    p[0] = (pack(command
                 + rs_reg('e') + nl() + 'ADD e c' + nl()
                 + "SUB e d" + nl()
                 + 'JZERO e ' + jump_label[m1] + nl()  # jesli zero to m1
                 + 'JUMP ' + jump_label[m2] + nl()  # jesli nie zero to m2
                 + m1
                 , '<<GEQ'), m2)


def p_condition_leq(p):
    """condition   : value LEQ value"""
    command = standard_render(p[1], p[3], 'c', 'd', str(p.lineno(2)))
    m1, m2 = get_marks(2)
    p[0] = (pack(command
                 + rs_reg('e') + nl() + 'ADD e c' + nl()
                 + "SUB e d" + nl()
                 + 'JZERO e ' + jump_label[m1] + nl()  # jesli zero to m1
                 + 'JUMP ' + jump_label[m2] + nl()  # jesli nie zero to m2( podane wyzej)
                 + m1
                 , '<<LEQ'), m2)


def p_condition_eq(p):
    """condition   : value EQ value"""
    command = standard_render(p[1], p[3], 'c', 'd', str(p.lineno(2)))
    m1, m2, m3 = get_marks(3)
    p[0] = (pack(command
                 + rs_reg('e') + nl() + 'ADD e c' + nl()
                 + rs_reg('f') + nl() + 'ADD f d' + nl()
                 + "SUB e d" + nl()
                 + "SUB f c" + nl()
                 + 'JZERO e ' + jump_label[m3] + nl()
                 + 'JUMP ' + jump_label[m2] + nl()
                 + m3 + 'JZERO f ' + jump_label[m1] + nl()
                 + 'JUMP ' + jump_label[m2] + nl()
                 + m1
                 , '<<EQ'), m2)


# TODO: NEQ
def p_condition_neq(p):
    """condition   : value NEQ value"""
    command = standard_render(p[1], p[3], 'c', 'd', str(p.lineno(2)))
    m1, m2, m3 = get_marks(3)
    p[0] = (pack(command
                 + rs_reg('e') + nl() + 'ADD e c' + nl()
                 + rs_reg('f') + nl() + 'ADD f d' + nl()
                 + "SUB e d" + nl()
                 + "SUB f c" + nl()
                 + 'JZERO e ' + jump_label[m3] + nl()
                 + 'JUMP ' + jump_label[m1] + nl()
                 + m3 + 'JZERO f ' + jump_label[m2] + nl()
                 + 'JUMP ' + jump_label[m1] + nl()
                 + m1
                 , '<<NEQ'), m2)


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


def p_identifier_table_id(p):
    '''identifier   : ID LBR ID RBR '''
    p[0] = ("arr", p[1], ("id", p[3]))


def p_identifier(p):
    '''identifier	: ID LBR NUM RBR '''
    p[0] = ("arr", p[1], ("num", p[3]))


def p_error(p):
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    raise Exception('Syntax error in input! Parser State:{} {} . {}'
                    .format(parser.state,
                            stack_state_str,
                            p))


parser = ply.yacc.yacc()


def test_compiler(f1='../my_tests/test', f2='result.mr'):
    f = open(f1, "r")
    parsed = parser.parse(f.read(), tracking=True)
    fw = open(f2, "w")
    clear = unpack(parsed)
    no_labels = remove_marks(unpack(parsed), jump_label)
    fw.write(no_labels)
    fw.close()
    os.system('../virtual_machine/maszyna-wirtualna result.mr')


test_compiler(f1='../examples/tests/program0.imp')
