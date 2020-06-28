from typing import Callable, NamedTuple, Tuple
from enum import Enum, unique
from error import ParseError


@unique
class TokenType(Enum):
    """Constants enumeration for Py-Dician's token types.

    Parameters:
        symbol (str): the symbol for that token type.
                      May be None if it's not represented by a symbol.
    """

    END = (None, )
    PLUS = ('+', )
    MINUS = ('-', )
    MULTIPLY = ('*', )
    DIVIDE = ('/', )
    LEFT_PARENTHESIS = ('(', )
    RIGHT_PARENTHESIS = (')', )
    DIE = ('d', )
    INTEGER = (None, )

    def __new__(cls, symbol: str):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__)
        obj.symbol = symbol
        return obj

    def __str__(self) -> str:
        return self.symbol if self.symbol else f'<{self.name}>'


@unique
class Closure(Enum):
    """Py-Dician's closures (pairs of tokens that enclose expressions).

    Parameters:
        begin (TokenType): the type of token that opens the closure.
        end (TokenType): the type of token that closes the closure.
    """

    PARENTHESES = (TokenType.LEFT_PARENTHESIS, TokenType.RIGHT_PARENTHESIS)

    def __new__(cls, begin: TokenType, end: TokenType):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__)
        obj.begin = begin
        obj.end = end
        return obj

    def __str__(self) -> str:
        return str((str(self.begin), str(self.end)))


class Token():
    """Class that represents a Py-Dician token, extracted from a string.

    Parameters:
        type (TokenType): a member from the TokenType enum representing the token's type.
        value (str): the value of the token, extracted from the string.
        line (int): the line at which the token starts.
        column (int): the position in the line at which the token starts.
    """

    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return self.value if self.value else str(self.type)


class EndOfStringError(ParseError):
    """Exception thrown by the Tokenizer class when the parse reaches the end of the parsed string.

    Parameters:
        line (int): the line at which the string ends.
        column (int): the position in the line at which the string ends.
    """

    pass


class UnknownSymbolError(ParseError):
    """Exception thrown by the Tokenizer class when it finds a symbol for which there's no defined token type.

    Parameters:
        symbol (str): the unknown symbol that was found.
        line (int): the line where the symbol was found.
        column (int): the position where the symbol was found in the line.
    """

    def __init__(self, symbol: str, line: int, column: int):
        super().__init__(line, column)
        self.symbol = symbol


class Tokenizer():
    """Class that parses a string accordingly to Py-Dician, fetching each token sequentially.

    Parameters:
        [optional] input_string (str): the string to be parsed. The default-value is an empty string, i.e. no string to parse.
    """

    def __init__(self, input_string: str = ''):
        self.set_input_string(input_string)

    def set_input_string(self, input_string: str) -> None:
        """Sets the string to be parsed and resets the parsing.

        Parameters:
            input_string (str): the string to be parsed.
        """

        self._input_string = input_string
        self.reset()

    def reset(self) -> None:
        """Resets the parsing to the beginning of the string."""

        self._current_symbol = self._input_string[0:1]
        self._current_index = 0
        self._current_line = 1
        self._current_column = 1
        self._begin_token()

    def next_token(self) -> Token:
        """Fetches the next token from the parsed string.

        Returns:
            A Token object containing the fetched token.
            If the end of the string is reached, an END (TokenType) token is returned.

        Raises:
            UnknownSymbolError if an unknown symbol is found.
        """

        try:
            self._skip_blanks()
            self._begin_token()

            if self._expect_symbol_is_any_of(TokenType.LEFT_PARENTHESIS):
                return self._fetch_token(TokenType.LEFT_PARENTHESIS)

            if self._expect_symbol_is_any_of(TokenType.RIGHT_PARENTHESIS):
                return self._fetch_token(TokenType.RIGHT_PARENTHESIS)

            if self._expect_symbol_is_any_of(TokenType.PLUS):
                return self._fetch_token(TokenType.PLUS)

            if self._expect_symbol_is_any_of(TokenType.MINUS):
                return self._fetch_token(TokenType.MINUS)

            if self._expect_symbol_is_any_of(TokenType.MULTIPLY):
                return self._fetch_token(TokenType.MULTIPLY)

            if self._expect_symbol_is_any_of(TokenType.DIVIDE):
                return self._fetch_token(TokenType.DIVIDE)

            if self._expect_symbol_is_any_of(TokenType.DIE):
                return self._fetch_token(TokenType.DIE)

            if self._expect_symbol_is_any_digit():
                return self._fetch_integer()

            self._raise_unknown_symbol_error()
        except EndOfStringError:
            return self._fetch_token(TokenType.END)

    def _raise_unknown_symbol_error(self) -> None:
        # Raises an UnknownSymbolError exception for the current symbol.

        unknown_symbol_error = UnknownSymbolError(self._current_symbol, self._current_line, self._current_column)

        self._next_symbol()
        self._begin_token()

        raise unknown_symbol_error

    def _fetch_integer(self) -> Token:
        # Fetches an INTEGER (TokenType) token, starting at the current symbol.

        self._skip_digits()
        return self._fetch_token(TokenType.INTEGER)

    def _has_symbols_left(self) -> bool:
        return self._current_index < len(self._input_string)

    def _next_symbol(self) -> None:
        # Advances the parsing to next character of the parsed string.

        if not self._has_symbols_left():
            raise EndOfStringError(self._current_line, self._current_column)

        self._current_index += 1
        if self._current_symbol == '\n':
            self._current_line += 1
            self._current_column  = 1
        else:
            self._current_column += 1

        self._current_symbol = self._input_string[self._current_index : self._current_index+1].casefold()

    def _begin_token(self) -> None:
        # Begins a new current token.

        self._token_start = self._current_index
        self._token_line = self._current_line
        self._token_column = self._current_column

    def _skip_symbols_while(self, condition: Callable[[str], bool]) -> None:
        # Skips symbols in the parsed string while they satisfy a given condition.

        while self._has_symbols_left():
            if condition(self._current_symbol):
                self._next_symbol()
            else:
                break

    def _skip_blanks(self) -> None:
        # Skips blanks (symbol.isspace() == True) in the parsed string.

        self._skip_symbols_while(lambda x: x.isspace())

    def _skip_digits(self) -> None:
        # Skips digits (symbol.isdigit() == True) in the parsed string.

        self._skip_symbols_while(lambda x: x.isdigit())

    def _fetch_token(self, token_type: TokenType) -> Token:
        # Returns the current token and begins a new one.

        token_value = self._input_string[self._token_start : self._current_index]
        token = Token(token_type, token_value, self._token_line, self._token_column)

        self._begin_token()

        return token

    def _expect_symbol_is_any_of(self, *expected_symbols: Tuple[TokenType, ...]) -> bool:
        # Checks if the current symbol is any of a given set. If it is, advances to the next symbol.

        if not any((x.symbol==self._current_symbol for x in expected_symbols)):
            return False

        self._next_symbol()

        return True

    def _expect_symbol_is_any_digit(self) -> bool:
        # Checks if the symbol a digit. If it is, advances to the next symbol.

        return self._expect_symbol_is(lambda symbol: symbol.isdigit())

    def _expect_symbol_is(self, condition: Callable[[str], bool]) -> bool:
        # Checks if the current symbol satisfies a given condition. If it does, advances to the next symbol.

        if not condition(self._current_symbol):
            return False

        self._next_symbol()

        return True
