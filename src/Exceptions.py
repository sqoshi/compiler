class TakenVariableNameException(Exception):
    def __init__(self, var=None, line_no=None, message="Variable name is taken."):
        if var and line_no:
            message = "Error in line {}. Variable name {} is taken.".format(line_no, var)
        super().__init__(message)


class VariableNotDeclaredException(Exception):
    def __init__(self, var=None, line_no=None, message="Variable were not declared."):
        if var and line_no:
            message = "Error in line {}. Variable {} were not declared.".format(line_no, var)
        super().__init__(message)


