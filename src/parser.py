import os
import re
import ply.yacc
from src.Exceptions import *
from src.lexer import lexer, tokens

memory_counter = 1
arrays = dict()
variables = dict()
initialized = set()
jump_label = dict()

tags = False


def label_to_line(text):
    stack = list(jump_label.keys())
    line_no = dict()
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for k in stack:
            if k in line:
                line_no[k] = i
                lines[i] = lines[i].replace(k, "")
    for i, line in enumerate(lines):
        for k, v in jump_label.items():
            if v in line:
                lines[i] = line.replace(v, str(line_no[k] - i))
    result = '\n'.join(lines)
    return result


def mark():
    val = len(jump_label)
    key = '~~LABELJUMPTO>' + str(val) + '<~~'
    jump_label[key] = '~~LABEL>' + str(val) + '<~~'
    return key


def clarify(text: str) -> str:
    output = ""
    for line in text.split("\n"):
        if line != '':
            output += line.lstrip() + "\n"
    return output


def render_vaules_double(p, reg1, reg2):
    return render_val(p[1], str(p.lineno(1)), reg1) + render_val(p[3], str(p.lineno(1)), reg2)


def render_operation(*args):
    return ' '.join(args)


def add_nl(word):
    return str(word) + "\n"


def nl() -> str:
    return "\n"


def pack(txt, tag="##"):
    if tags:
        return tag + " " + txt + " " + tag[::-1]
    else:
        return txt


def is_id(variable):
    if variable[0] == 'id':
        return True


def is_arr(variable):
    if variable[0] == 'arr':
        return True


def is_num(variable):
    if variable[0] == 'num':
        return True


################################################################
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


def rs_reg(reg):
    return 'RESET ' + str(reg)


###########################################################################
######################### variable validation #############################
###########################################################################
def is_initialized(id, line):
    """ Check if variable was initialized. """
    if id not in initialized:
        raise VariableNotInitializedException(var=id, line=line)


def validate_var_addr(id, line):
    """ Check  if var was properly used and declared."""
    if id not in variables.keys():
        if id in arrays:
            raise TypeError('Error in line {}. Wrong usage of table variable {}.'.format(id, line))
        else:
            raise VariableNotDeclaredException(id, line)


def is_var_taken(id, line):
    """ Check if id is taken."""
    if id in variables.keys():
        raise TakenVariableNameException(var=id, line=line)


def is_var_declared(id, line):
    """ Check if variable were declared before use."""
    if id not in variables.keys():
        raise VariableNotDeclaredException(var=id, line=line)


def validate_indexes_array(idx1, idx2, line, id):
    """ Check if array indexes are valid."""
    if idx1 > idx2:
        raise IndexError('Error in line {}. Array {} indexes are wrong. ({}:{})'.format(line, id, idx1, idx2))


############################################################################

def add_arr(id, idx1, idx2, line):
    """ Save arr by id in memory and increase memory counter by array length."""
    validate_indexes_array(idx1, idx2, line, id)
    global memory_counter
    arrays[id] = (memory_counter + 1, idx1, idx2)
    inc_memory_counter(idx2 - idx1 + 1)


def get_var(id, line):
    is_var_declared(id, line)
    return variables[id]


def add_var(id, line):
    """ Save variable by id in memory and increase memory counter by 1."""
    inc_memory_counter()
    is_var_taken(id, line)
    variables[id] = get_memory_counter()


def rm_var(id):
    """ Remove variable from memory."""
    variables.pop(id)


def generate_number(number, reg):
    commands = ""
    while number != 0:
        if number % 2 == 0:
            number = number // 2
            commands = render_operation("SHL", reg, nl(), commands)
        else:
            number -= 1
            commands = render_operation("INC", reg, nl(), commands)
    commands = render_operation(rs_reg(reg), nl(), commands)
    return commands


def render_addr(variable, line, reg="b") -> str:
    if variable[0] == "id":
        validate_var_addr(variable[1], line)
        return generate_number(variables[variable[1]], reg)


def render_val(variable, line, reg="a") -> str:
    if is_num(variable):
        return generate_number(int(variable[1]), reg)
    elif is_id(variable):
        is_initialized(variable[1], line)
    return render_addr(variable, line, reg)


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
    id, line = p[3], str(p.lineno(3))
    add_var(id, line)


def p_declarations_array_rec(p):
    '''declarations : declarations COMMA ID LBR NUM COLON NUM RBR'''
    add_arr(p[3], p[5], p[7], str(p.lineno(3)))


def p_declarations_variable(p):
    '''declarations : ID'''
    id, line = p[1], str(p.lineno(1))
    add_var(id, line)


def p_declarations_array(p):
    '''declarations : ID LBR NUM COLON NUM RBR'''
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
    identifier, expression, line = p[1], p[3], str(p.lineno(1))
    p[0] = pack(str(expression) + render_addr(identifier, line, "b") + "STORE a b" + nl(), '<<asg')
    initialized.add(identifier[1])


def p_command_write(p):
    '''command	: WRITE value SEMICOLON '''
    p[0] = pack(render_val(p[2], str(p.lineno(1)), "b") + 'PUT b' + nl(), '<<write')


def p_command_read(p):
    '''command	: READ identifier SEMICOLON '''
    initialized.add(p[2][1])
    p[0] = render_addr(p[2], str(p.lineno(1)), "b") + "GET b" + nl()


##################################################################
####################### expression ###############################
##################################################################

def p_expression_value(p):
    '''expression   : value'''
    p[0] = pack(render_val(p[1], str(p.lineno(1)), "a"), "<<valexp")


def p_expression_plus(p):
    '''expression   : value PLUS value'''
    command = render_vaules_double(p, 'a', 'c')
    if is_id(p[1]):
        command += "LOAD a a" + nl()
    if is_id(p[3]):
        command += "LOAD c c" + nl()
    p[0] = pack(command + "ADD a c" + nl(), '<<plus')


def p_expression_minus(p):
    '''expression   : value MINUS value'''
    command = render_vaules_double(p, 'a', 'c')
    if is_id(p[1]):
        command += "LOAD a a" + nl()
    if is_id(p[3]):
        command += "LOAD c c" + nl()
    p[0] = pack(command + "SUB a c" + nl(), '<<minus')


def p_expression_multiplication(p):
    '''expression   : value MULT value'''
    command = render_vaules_double(p, 'd', 'c')
    if is_id(p[1]):
        command += "LOAD d d" + nl()
    if is_id(p[3]):
        command += "LOAD c c" + nl()
    m1 = mark()
    m2 = mark()
    m3 = mark()
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
    '''expression   : value DIV value'''
    command = render_vaules_double(p, 'b', 'c')
    if is_id(p[1]):
        command += "LOAD b b" + nl()
    if is_id(p[3]):
        command += "LOAD c c" + nl()
    m0 = mark()
    m1 = mark()
    m2 = mark()
    m3 = mark()
    m4 = mark()
    m5 = mark()
    m6 = mark()
    p[0] = pack(command
                + "JZERO d " + jump_label[m6] + nl()
                + rs_reg('d') + nl() + "INC d" + nl()
                + m0 + rs_reg('f') + nl() + rs_reg('a') + nl() + "SUB a f" + nl()
                + "SUB a c" + nl() + "JZERO a " + jump_label[m1] + nl() + "ADD c c" + nl() + "ADD d d" + nl()
                + "JUMP " + jump_label[m0] + nl() + m1 + rs_reg('e') + nl() + rs_reg('a') + nl() + "SUB a e" + nl()
                , '<<div')


##################################################################
######################## condition ###############################
##################################################################


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


def test_compiler(f1='../test', f2='result.mr'):
    f = open(f1, "r")
    parsed = parser.parse(f.read(), tracking=True)
    fw = open(f2, "w")
    clear = clarify(parsed)
    no_labels = label_to_line(clarify(parsed))
    fw.write(no_labels)
    fw.close()
    os.system('../virtual_machine/maszyna-wirtualna result.mr')


test_compiler()
