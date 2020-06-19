class PyDicianError(Exception):
    """Base-class for Py-Dician errors."""

    pass


class ParseError(PyDicianError):
    """Base-class for parse errors, either of lexical, syntactic or semantic nature.

    Parameters:
        line (int): the line at which the error occurred.
        column (int): the position in the line at which the error occurred.
    """

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column
