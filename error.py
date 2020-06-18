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

    def __str__(self) -> str:
        return f'[Error] Ln {self.line}, Col {self.column}: {self.code}'
