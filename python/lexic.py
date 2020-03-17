import enum


SYMBOL_LEFT_PARENTHESIS = '('
SYMBOL_RIGHT_PARENTHESIS = ')'
SYMBOL_PLUS = '+'
SYMBOL_MINUS = '-'
SYMBOL_MULTIPLY = '*'
SYMBOL_DIVIDE = '/'
KEYWORD_DIE = 'd'


class TokenType(enum.Enum):
    END = enum.auto()
    LEFT_PARENTHESIS = enum.auto()
    RIGHT_PARENTHESIS = enum.auto()
    PLUS = enum.auto()
    MINUS = enum.auto()
    MULTIPLY = enum.auto()
    DIVIDE = enum.auto()
    INTEGER = enum.auto()
    DIE = enum.auto()

    def __repr__(self):
        return f'<{self.__class__.__name__}.{self.name}>'

    def __str__(self):
        return self.name


class Token():
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'{self.__class__.__name__}(kind={self.kind}, value="{self.value}", line={self.line}, column={self.column})'

    def __str__(self):
        return str(self.value)


class TokenizerError(Exception):
    pass


class EndOfTextError(TokenizerError):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def __repr__(self):
        return f'{self.__class__.__name__}(line={self.line}, column={self.column})'

    def __str__(self):
        return f'Ln {self.line}, Col {self.column}: reached the end of the input string.'


class UnexpectedSymbolError(TokenizerError):
    def __init__(self, symbol, line, column):
        self.symbol = symbol
        self.line = line
        self.column = column

    def __repr__(self):
        return f'{self.__class__.__name__}(symbol="{self.symbol}", line={self.line}, column={self.column})'

    def __str__(self):
        return f'Ln {self.line}, Col {self.column}: "{self.symbol}": unexpected symbol.'


class Tokenizer():
    def __init__(self, input_string=''):
        self.set_input_string(input_string)

    def set_input_string(self, input_string):
        self._input_string = input_string
        self._current_symbol = self._input_string[0:1]
        self._current_index = 0
        self._current_line = 1
        self._current_column = 1
        self._begin_token()

    def next_token(self):
        try:
            self._skip_blanks()
            self._begin_token()

            if self._expect_symbol_is_any_of(SYMBOL_LEFT_PARENTHESIS):
                return self._fetch_token(TokenType.LEFT_PARENTHESIS)

            if self._expect_symbol_is_any_of(SYMBOL_RIGHT_PARENTHESIS):
                return self._fetch_token(TokenType.RIGHT_PARENTHESIS)

            if self._expect_symbol_is_any_of(SYMBOL_PLUS):
                return self._fetch_token(TokenType.PLUS)

            if self._expect_symbol_is_any_of(SYMBOL_MINUS):
                return self._fetch_token(TokenType.MINUS)

            if self._expect_symbol_is_any_of(SYMBOL_MULTIPLY):
                return self._fetch_token(TokenType.MULTIPLY)

            if self._expect_symbol_is_any_of(SYMBOL_DIVIDE):
                return self._fetch_token(TokenType.DIVIDE)

            if self._expect_symbol_is_any_of(KEYWORD_DIE):
                return self._fetch_token(TokenType.DIE)

            if self._expect_symbol_is_any_digit():
                return self._fetch_integer()

            self._raise_unexpected_symbol_error()
        except EndOfTextError:
            return self._fetch_token(TokenType.END)

    def _raise_unexpected_symbol_error(self):
        unknown_symbol_error = UnexpectedSymbolError(self._current_symbol, self._current_line, self._current_column)

        self._next_symbol()
        self._begin_token()

        raise unknown_symbol_error

    def _fetch_integer(self):
        self._skip_digits()
        return self._fetch_token(TokenType.INTEGER)

    def _has_symbols_left(self):
        return self._current_index < len(self._input_string)

    def _next_symbol(self):
        if not self._has_symbols_left():
            raise EndOfTextError(self._current_line, self._current_column)

        self._current_index += 1
        if self._current_symbol == '\n':
            self._current_line += 1
            self._current_column  = 1
        else:
            self._current_column += 1

        self._current_symbol = self._input_string[self._current_index : self._current_index+1].casefold()

    def _begin_token(self):
        self._token_start = self._current_index
        self._token_line = self._current_line
        self._token_column = self._current_column

    def _skip_symbols_while(self, condition):
        while self._has_symbols_left():
            if condition(self._current_symbol):
                self._next_symbol()
            else:
                break

    def _skip_blanks(self):
        self._skip_symbols_while(lambda x: x.isspace())

    def _skip_digits(self):
        self._skip_symbols_while(lambda x: x.isdigit())

    def _fetch_token(self, kind):
        token_value = self._input_string[self._token_start : self._current_index]
        token = Token(kind, token_value, self._token_line, self._token_column)

        self._begin_token()

        return token

    def _expect_symbol_is_any_of(self, *expected_symbols):
        return self._expect_symbol_is(lambda symbol: symbol in expected_symbols)

    def _expect_symbol_is_any_digit(self):
        return self._expect_symbol_is(lambda symbol: symbol.isdigit())

    def _expect_symbol_is(self, condition):
        if not condition(self._current_symbol):
            return False

        self._next_symbol()

        return True

if __name__ == '__main__':
    tkr = Tokenizer('2d10 + d6 - 3')
    try:
        keep_fetching = True
        while keep_fetching:
            token = tkr.next_token()
            print(token)
            keep_fetching = token.kind!=TokenType.END
    except TokenizerError as e:
        print(e)
