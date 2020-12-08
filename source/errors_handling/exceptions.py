class TakenVariableNameException(Exception):
    def __init__(self, var=None, line=None, message="Variable name is taken."):
        if var and line:
            message = "Error in line {}. Variable name {} is taken.".format(line, var)
        super().__init__(message)


class VariableNotDeclaredException(Exception):
    def __init__(self, var=None, line=None, message="Variable were not declared."):
        if var and line:
            message = "Error in line {}. Variable {} were not declared.".format(line, var)
        super().__init__(message)


class VariableNotInitializedException(Exception):
    def __init__(self, var=None, line=None, message="Variable were not initialized."):
        if var and line:
            message = "Error in line {}. Variable {} were not initialized.".format(line, var)
        super().__init__(message)


class IteratorAssignException(Exception):
    def __init__(self, var=None, line=None, message="Iterator assign value attempt."):
        if var and line:
            message = "Error in line {}. You cannot assign value to iterator {}.".format(line, var)
        super().__init__(message)


class WrongVariableUsageException(Exception):
    def __init__(self, var=None, line=None, message="Incorrect use of {} variable."):
        if var and line:
            message = "Error in line {}. Incorrect use of {} variable.".format(line, var)
        super().__init__(message)
