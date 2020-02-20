from enum import Enum, auto

SYMBOL_PLUS  = '+'
SYMBOL_MINUS = '-'
KEYWORD_D    = 'd'

class TokenType(Enum):
    SB_PLUS  = auto()
    SB_MINUS = auto()
    INTEGER  = auto()
    KW_D     = auto()

    def issymbol(self):
        return self == TokenType.SB_PLUS or self == TokenType.SB_MINUS

    def iskeyword(self):
        return self == TokenType.KW_D
    
    def isliteral(self):
        return self == TokenType.INTEGER

    def __str__(self):
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

class Tokenizer():
    def __init__(self, text = ''):
        self.parse(text)

    def parse(self, text):
        self._text          = text
        self._current_index = 0
        self._token_start   = 0

    def fetch(self):
        self._skipblanks()

        current = self._read()

        if self._issymbolplus(current):
            return self._getplus()

        if self._issymbolminus(current):
            return self._getminus()

        if self._iskeywordd(current):
            return self._getdice()

        if current.isdigit():
            return self._readinteger()

        return None

    def _readinteger(self):
        self._skipdigits()
        return self._getinteger()

    def _hassymbolsleft(self):
        return self._current_index < len(self._text)
    
    def _peek(self):
        if self._hassymbolsleft():
            return self._text[self._current_index]

        return '\x00'

    def _read(self):
        symbol = self._peek()

        if symbol != '\x00':
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
    tkr   = Tokenizer('2d10 + d6 - 3')
    token = tkr.fetch()

    while token != None:
        print(token)

        token = tkr.fetch()
