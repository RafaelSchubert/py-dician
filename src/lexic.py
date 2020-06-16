from typing import Callable, Tuple
import enum


class Symbol(str, enum.Enum):
    """Base-class enumeration of the symbols of the dice-language."""

    def __str__(self) -> str:
        return self.value


@enum.unique
class Sign(Symbol):
    """Constants enumeration of the signs (single-character symbols) of the dice-language."""

    LEFT_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'


@enum.unique
class Keyword(Symbol):
    """Constants enumeration of the keywords (reserved identifiers) of the dice-language."""

    DIE = 'd'


class TokenType(enum.IntEnum):
    """Constants enumeration for the possible types of tokens of the dice-language."""

    END = enum.auto()
    LEFT_PARENTHESIS = enum.auto()
    RIGHT_PARENTHESIS = enum.auto()
    PLUS = enum.auto()
    MINUS = enum.auto()
    MULTIPLY = enum.auto()
    DIVIDE = enum.auto()
    INTEGER = enum.auto()
    DIE = enum.auto()

    def __str__(self) -> str:
        return self.name


class Token():
    """Class that represents a token of the dice-language, extracted from a string."""

    def __init__(self, kind: TokenType, value: str, line: int, column: int):
        """
        Builds an object from the token's type, value and position where it was found.

        Parameters:
            kind (TokenType): a member from the TokenType enum representing the token's type.
            value (str): the value of the token, extracted from the string.
            line (int): the line at which the token starts.
            column (int): the position in the line at which the token starts.
        """

        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(kind={self.kind.name}, value="{self.value}", line={self.line}, column={self.column})'

    def __str__(self) -> str:
        return self.value


class TokenizerError(Exception):
    """Base-class for the Tokenizer class' exceptions."""

    pass


class EndOfTextError(TokenizerError):
    """Exception thrown by the Tokenizer class when the parsing reaches the end of the parsed string."""

    def __init__(self, line: int, column: int):
        """
        Builds an object from the position where the parsed string ends.

        Parameters:
            line (int): the line at which the string ends.
            column (int): the position in the line at which the string ends.
        """

        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(line={self.line}, column={self.column})'

    def __str__(self) -> str:
        return f'Ln {self.line}, Col {self.column}: reached the end of the input string.'


class UnknownSymbolError(TokenizerError):
    """Exception thrown by the Tokenizer class when it finds a symbol for which there's no defined token type."""

    def __init__(self, symbol: str, line: int, column: int):
        """
        Builds an object from the symbol and the position where it was found.

        Parameters:
            symbol (str): the unknown symbol that was found.
            line (int): the line where the symbol was found.
            column (int): the position where the symbol was found in the line.
        """

        self.symbol = symbol
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(symbol="{self.symbol}", line={self.line}, column={self.column})'

    def __str__(self) -> str:
        return f'Ln {self.line}, Col {self.column}: "{self.symbol}": unknown symbol.'


class Tokenizer():
    """Class that parses a string accordingly to the dice-language, fetching each token sequentially."""

    def __init__(self, input_string: str = ''):
        """
        Builds an object and initializes it with a string to be parsed.

        Parameters:
            input_string (str): the string to be parsed. The default-value is an empty string, i.e. no string to parse.
        """

        self.set_input_string(input_string)

    def set_input_string(self, input_string: str) -> None:
        """
        Sets the string to be parsed and resets the parsing.

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
        """
        Fetches the next token from the parsed string.

        Returns:
            A Token object containing the fetched token.
            If the end of the string is reached, an END (TokenType) token is returned.

        Raises:
            UnknownSymbolError if an unknown symbol is found.
        """

        try:
            self._skip_blanks()
            self._begin_token()

            if self._expect_symbol_is_any_of(Sign.LEFT_PARENTHESIS):
                return self._fetch_token(TokenType.LEFT_PARENTHESIS)

            if self._expect_symbol_is_any_of(Sign.RIGHT_PARENTHESIS):
                return self._fetch_token(TokenType.RIGHT_PARENTHESIS)

            if self._expect_symbol_is_any_of(Sign.PLUS):
                return self._fetch_token(TokenType.PLUS)

            if self._expect_symbol_is_any_of(Sign.MINUS):
                return self._fetch_token(TokenType.MINUS)

            if self._expect_symbol_is_any_of(Sign.MULTIPLY):
                return self._fetch_token(TokenType.MULTIPLY)

            if self._expect_symbol_is_any_of(Sign.DIVIDE):
                return self._fetch_token(TokenType.DIVIDE)

            if self._expect_symbol_is_any_of(Keyword.DIE):
                return self._fetch_token(TokenType.DIE)

            if self._expect_symbol_is_any_digit():
                return self._fetch_integer()

            self._raise_unknown_symbol_error()
        except EndOfTextError:
            return self._fetch_token(TokenType.END)

    def _raise_unknown_symbol_error(self) -> None:
        """Raises an UnknownSymbolError exception for the current symbol."""
        unknown_symbol_error = UnknownSymbolError(self._current_symbol, self._current_line, self._current_column)

        self._next_symbol()
        self._begin_token()

        raise unknown_symbol_error

    def _fetch_integer(self) -> Token:
        """
        Fetches an INTEGER (TokenType) token, starting at the current symbol.

        Returns:
            A Token object containing the fetched token.
        """

        self._skip_digits()
        return self._fetch_token(TokenType.INTEGER)

    def _has_symbols_left(self) -> bool:
        """
        Checks if the parsing reached the end of the parsed string.

        Returns:
            True if the end of the parsed string was reached. False, otherwise.
        """

        return self._current_index < len(self._input_string)

    def _next_symbol(self) -> None:
        """
        Advances the parsing to next character of the parsed string.

        Raises:
            EndOfTextError if currently at the end of the parsed string.
        """

        if not self._has_symbols_left():
            raise EndOfTextError(self._current_line, self._current_column)

        self._current_index += 1
        if self._current_symbol == '\n':
            self._current_line += 1
            self._current_column  = 1
        else:
            self._current_column += 1

        self._current_symbol = self._input_string[self._current_index : self._current_index+1].casefold()

    def _begin_token(self) -> None:
        """Begins a new current token."""

        self._token_start = self._current_index
        self._token_line = self._current_line
        self._token_column = self._current_column

    def _skip_symbols_while(self, condition: Callable[[str], bool]) -> None:
        """
        Skips symbols in the parsed string while they satisfy a given condition.

        Parameters:
            condition (Callable[[str], bool]): a callable that takes a string as an argument and returns a bool.
        """

        while self._has_symbols_left():
            if condition(self._current_symbol):
                self._next_symbol()
            else:
                break

    def _skip_blanks(self) -> None:
        """Skips blanks (symbol.isspace() == True) in the parsed string."""

        self._skip_symbols_while(lambda x: x.isspace())

    def _skip_digits(self) -> None:
        """Skips digits (symbol.isdigit() == True) in the parsed string."""

        self._skip_symbols_while(lambda x: x.isdigit())

    def _fetch_token(self, kind: TokenType) -> Token:
        """
        Returns the current token and begins a new one.

        Parameters:
            kind (TokenType): a type to be assigned to the fetched token.

        Returns:
            A Token object containing the fetched token.
        """

        token_value = self._input_string[self._token_start : self._current_index]
        token = Token(kind, token_value, self._token_line, self._token_column)

        self._begin_token()

        return token

    def _expect_symbol_is_any_of(self, *expected_symbols: Tuple[str, ...]) -> bool:
        """
        Checks if the current symbol is any of a given set. If it is, advances to the next symbol.

        Parameters:
            expected_symbols (Tuple[str, ...]): a tuple of strings containing a set of possible symbols.

        Returns:
            True if the current symbol is any of those in expected_symbols. False, otherwise.
        """

        return self._expect_symbol_is(lambda symbol: symbol in expected_symbols)

    def _expect_symbol_is_any_digit(self) -> bool:
        """
        Checks if the symbol a digit. If it is, advances to the next symbol.

        Returns:
            True if the current symbol is a digit. False, otherwise.
        """

        return self._expect_symbol_is(lambda symbol: symbol.isdigit())

    def _expect_symbol_is(self, condition: Callable[[str], bool]) -> bool:
        """
        Checks if the current symbol satisfies a given condition. If it does, advances to the next symbol.

        Parameters:
            condition (Callable[[str], bool]): a callable that takes a string as an argument and returns a bool.

        Returns:
            True if condition() returns True for the current symbol. False, otherwise.
        """

        if not condition(self._current_symbol):
            return False

        self._next_symbol()

        return True
