from enum import Enum, auto

class TokenType(Enum):
    SB_PLUS  = auto()
    SB_MINUS = auto()
    INTEGER  = auto()
    KW_D     = auto()

class Token():
    def __init__(self, kind = None, value = None):
        self.kind  = kind
        self.value = value

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
            return self._getinteger()

        return None

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

    def _skipblanks(self):
        while self._hassymbolsleft():
            if self._peek().isspace():
                self._current_index += 1
            else:
                break

    def _skip_digits(self):
        while self._hassymbolsleft():
            if self._peek().isdigit():
                self._current_index += 1
            else:
                break

    def _tokenstring(self):
        return self._text[self._token_start:self._current_index]

    def _extracttoken(self, kind, value = None):
        token = Token(kind, value)

        self._token_start = self._current_index

        return token

    def _getplus(self):
        return self._extracttoken(TokenType.SB_PLUS)

    def _getminus(self):
        return self._extracttoken(TokenType.SB_MINUS)

    def _getinteger(self):
        return self._extracttoken(TokenType.INTEGER, int(self._tokenstring()))

    def _getdice(self):
        return self._extracttoken(TokenType.KW_D)

    def _issymbolplus(self, token):
        return token == '+'

    def _issymbolminus(self, token):
        return token == '-'

    def _iskeywordd(self, token):
        return token.casefold() == 'd'

if __name__ == '__main__':
    tkr   = Tokenizer('d5d6')
    token = tkr.fetch()

    while token != None:
        print(token.kind, token.value)

        token = tkr.fetch()
