from enum import Enum, unique, auto

class Token():
    @unique
    class Type(Enum):
        SB_PLUS  = auto()
        SB_MINUS = auto()
        INTEGER  = auto()
        DICE     = auto()

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
        if current != None:
            if current == '+':
                return self._getplus()
            if current == '-':
                return self._getminus()
            if current == '0':
                return self._getinteger()
            if current.casefold() == 'd':
                pass
            if current.isdigit():
                self._skip_digits()
                if self._peek() == 'd':
                    pass
                return self._getinteger()
        return Token()

    def _hassymbolsleft(self):
        return self._current_index < len(self._text) and self._state != Tokenizer.State.FINISHED
    
    def _peek(self):
        if self._hassymbolsleft():
            return self._text[self._current_index]
        return None

    def _read(self):
        symbol = self._peek()
        if symbol != None:
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
        return self._extracttoken(Token.Type.SB_PLUS)

    def _getminus(self):
        return self._extracttoken(Token.Type.SB_MINUS)

    def _getinteger(self):
        return self._extracttoken(Token.Type.INTEGER, int(self._tokenstring()))
