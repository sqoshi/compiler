import numpy

from source.beautify import concat, nl, mark
from source.errors_handling.exceptions import *

memory_counter = 1
arrays = dict()
variables = dict()
initialized = set()
jump_label = dict()
iterators_set = set()


################################################################################
############################## getters & setters ###############################
################################################################################

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


################################################################################
############################## validation ######################################
################################################################################
def is_id(variable):
    if variable[0] == 'id':
        return True


def is_arr(variable):
    if variable[0] == 'arr':
        return True


def is_num(variable):
    if variable[0] == 'num':
        return True


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


################################################################################
###################### management & operating ##################################
################################################################################

def get_var(id, line):
    """ Return the variable address. """
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


################################################################################
############################# code generating ##################################
################################################################################

def rs_reg(reg):
    return 'RESET ' + str(reg)


def get_marks(n):
    """ Generate multiple labels. """
    return tuple(mark(jump_label) for _ in numpy.arange(n))


def load_if_addr(command, val, via, to):
    if is_id(val):
        command += "LOAD {} {}".format(via, to) + nl()
    return command


def generate_number(number, reg):
    commands = ""
    while number != 0:
        if number % 2 == 0:
            number = number // 2
            commands = concat("SHL", reg, nl(), commands)
        else:
            number -= 1
            commands = concat("INC", reg, nl(), commands)
    commands = concat(rs_reg(reg), nl(), commands)
    return commands


def render_addr(variable, line, reg="b") -> str:
    if variable[0] == "id":
        validate_var_addr(variable[1], line)
        return generate_number(get_variables()[variable[1]], reg)


def render_value(variable, line, reg="a") -> str:
    if is_num(variable):
        return generate_number(int(variable[1]), reg)
    elif is_id(variable):
        is_initialized(variable[1], line)
    return render_addr(variable, line, reg)


def render_values_multiple(*args) -> str:
    result = ""
    for (pi, reg, lineno) in args:
        result = result + render_value(pi, str(int(lineno) + 2), reg)
    return result


def standard_render(p1, p2, r1, r2, lineno):
    command = render_values_multiple((p1, r1, lineno), (p2, r2, lineno))
    command = load_if_addr(command, p1, r1, r1)
    command = load_if_addr(command, p2, r2, r2)
    return command
