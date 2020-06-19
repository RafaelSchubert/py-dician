from enum import auto, IntEnum, unique

class PyDicianError(Exception):
    """Base-class for Py-Dician errors.

    Parameters:
        code (int): the integer ID of the error.
    """

    def __init__(self, code: int):
        self.code = code


class ParseError(PyDicianError):
    """Base-class for parse errors, either of lexical, syntactic or semantic nature.

    Parameters:
        code (int): the integer ID of the error.
        line (int): the line at which the error occurred.
        column (int): the position in the line at which the error occurred.
    """

    def __init__(self, code: int, line: int, column: int):
        super().__init__(code)
        self.line = line
        self.column = column


@unique
class ErrorCode(IntEnum):
    """Constants enumeration for the IDs of errors and warnings that may occur during the parse."""

    E_ENDOFSTRING = auto()
    E_LX_UNKNOWNSYMBOL = auto()
