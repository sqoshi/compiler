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
