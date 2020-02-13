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
                return self._extracttoken(Token.Type.SB_PLUS)
            if current == '-':
                return self._extracttoken(Token.Type.SB_MINUS)
            if current == '0':
                return self._extracttoken(Token.Type.INTEGER, 0)
            if current.casefold() == 'd':
                pass
            if current.isdigit():
                pass
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

    # def _skip_digits(self):
    #     while self._has_symbols_left():
    #         if self._peek_symbol().isdigit():
    #             self.symbol_index += 1
    #         else:
    #             break

    def _extracttoken(self, kind, value = None):
        token = Token(kind, value)
        self._token_start = self._current_index
        return token

#     def _start_token(self):
#         self.token_start = self.symbol_index

#     def _token_string(self):
#         return self.text[self.token_start:self.symbol_index]

#     def _fetch_token(self, tk_type):
#         token = (tk_type, (self.token_start, self.symbol_index), self._token_string())
#         self._start_token()
#         return token

#     def next(self):
#         self._skip_blanks()
#         self._start_token()
#         current = self._read_symbol()
#         if not current is None:
#             if current.casefold() == 'd':
#                 return self._fetch_token(Tokens.KeyWord_d)
#             if current == '+':
#                 return self._fetch_token(Tokens.Symbol_Plus)
#             if current == '-':
#                 return self._fetch_token(Tokens.Symbol_Minus)
#             if current == '(':
#                 return self._fetch_token(Tokens.Symbol_ParenthesisLeft)
#             if current == ')':
#                 return self._fetch_token(Tokens.Symbol_ParenthesisRight)
#             if current.isdigit():
#                 self._skip_digits()
#                 return self._fetch_token(Tokens.Literal_Integer)
#         return None
