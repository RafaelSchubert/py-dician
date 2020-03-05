from enum import Enum, auto

SYMBOL_PLUS  = '+'
SYMBOL_MINUS = '-'
KEYWORD_D    = 'd'

class TokenType(Enum):
    END      = auto()
    SB_PLUS  = auto()
    SB_MINUS = auto()
    INTEGER  = auto()
    KW_D     = auto()

    def isend(self):
        return self == TokenType.END

    def issymbol(self):
        return self == TokenType.SB_PLUS or self == TokenType.SB_MINUS

    def iskeyword(self):
        return self == TokenType.KW_D
    
    def isliteral(self):
        return self == TokenType.INTEGER

    def __str__(self):
        if self == TokenType.END:
            return 'End'

        if self == TokenType.SB_PLUS:
            return 'Plus'

        if self == TokenType.SB_MINUS:
            return 'Minus'

        if self == TokenType.KW_D:
            return 'Dice'

        if self == TokenType.INTEGER:
            return 'Integer'

        return 'None'

class Token():
    def __init__(self, kind = None, value = None):
        self.kind  = kind
        self.value = value

    def __str__(self):
        return str(self.value)

class TokenizerError(Exception):
    pass

class EndOfTextError(TokenizerError):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f'The end of the text was reached at position {self.position}.'

class UnexpectedSymbolError(TokenizerError):
    def __init__(self, symbol, position):
        self.symbol   = symbol
        self.position = position

    def __str__(self):
        return f'An unexpected symbol was found at position {self.position}. Symbol = "{self.symbol}".'

class Tokenizer():
    def __init__(self, text = ''):
        self.parse(text)

    def parse(self, text):
        self._text          = text
        self._current_index = 0
        self._token_start   = 0

    def fetch(self):
        self._skipblanks()

        try:
            current = self._read()
        except EndOfTextError:
            return Token(TokenType.END)

        if self._issymbolplus(current):
            return self._getplus()

        if self._issymbolminus(current):
            return self._getminus()

        if self._iskeywordd(current):
            return self._getdice()

        if current.isdigit():
            return self._readinteger()

        self._token_start = self._current_index

        raise UnexpectedSymbolError(current, self._current_index)

    def _readinteger(self):
        self._skipdigits()
        return self._getinteger()

    def _hassymbolsleft(self):
        return self._current_index < len(self._text)
    
    def _peek(self):
        if self._hassymbolsleft():
            return self._text[self._current_index]

        raise EndOfTextError(self._current_index)

    def _read(self):
        symbol = self._peek()

        self._current_index += 1
            
        return symbol

    def _skipwhile(self, condition):
        while self._hassymbolsleft():
            if condition(self._peek()):
                self._current_index += 1
            else:
                break

    def _skipblanks(self):
        self._skipwhile(lambda x: x.isspace())

    def _skipdigits(self):
        self._skipwhile(lambda x: x.isdigit())

    def _tokenstring(self):
        return self._text[self._token_start:self._current_index]

    def _extracttoken(self, kind, value = None):
        token = Token(kind, value)

        self._token_start = self._current_index

        return token

    def _getplus(self):
        return self._extracttoken(TokenType.SB_PLUS, SYMBOL_PLUS)

    def _getminus(self):
        return self._extracttoken(TokenType.SB_MINUS, SYMBOL_MINUS)

    def _getinteger(self):
        return self._extracttoken(TokenType.INTEGER, int(self._tokenstring()))

    def _getdice(self):
        return self._extracttoken(TokenType.KW_D, KEYWORD_D)

    def _issymbolplus(self, token):
        return token == SYMBOL_PLUS

    def _issymbolminus(self, token):
        return token == SYMBOL_MINUS

    def _iskeywordd(self, token):
        return token.casefold() == KEYWORD_D

if __name__ == '__main__':
    tkr = Tokenizer('2da10 f+ dh6 - 3')

    try:
        keep_fetching = True

        while keep_fetching:
            token = tkr.fetch()

            print(token)

            keep_fetching = not token.kind.isend()
    except TokenizerError as e:
        print(e)
