from enum import Enum, unique, auto

class Token():
    @unique
    class Type(Enum):
        SB_PLUS  = auto()
        SB_MINUS = auto()
        INTEGER  = auto()
        DICE     = auto()

    def __init__(self, kind = None, value = None):
        self._kind  = kind
        self._value = value

    def kind(self):
        return self._kind

    def value(self):
        return self._value

class Tokenizer():
    @unique
    class State(Enum):
        SEEKING_NEXT    = auto()
        ENDED           = auto()
        FOUND_DIGIT_NZ  = auto()
        READING_PLUS    = auto()
        READING_MINUS   = auto()
        READING_INTEGER = auto()
        READING_DICE    = auto()

    def __init__(self, text = ''):
        self.parse(text)

    def parse(self, text):
        self._text          = text
        self._state         = Tokenizer.State.SEEKING_NEXT
        self._current_index = 0
        self._token_start   = 0

    def fetch(self):
        while self._state != Tokenizer.State.ENDED:
            if self._state == Tokenizer.State.SEEKING_NEXT:
                self._seeknext()
            elif self._state == Tokenizer.State.READING_PLUS:
                pass
            elif self._state == Tokenizer.State.READING_MINUS:
                pass
        return Token()

    def _seeknext(self):
        self._skipblanks()
        current = self._peek()
        if current == None:
            self._state = Tokenizer.State.ENDED
        elif current == '+'
            self._state = Tokenizer.State.READING_PLUS
        elif current == '-':
            self._state = Tokenizer.State.READING_MINUS
        elif current == '0':
            self._state = Tokenizer.State.READING_INTEGER
        elif current.casefold() == 'd':
            self._state = Tokenizer.State.READING_DICE
        elif current.isdigit():
            self._state = Tokenizer.State.FOUND_DIGIT_NZ
        else:
            self._state = Tokenizer.State.ENDED

    def _getplus(self):
        pass

    def _getminus(self):
        pass

    def _hassymbolsleft(self):
        return self._current_index < len(self._text) and self._state != Tokenizer.State.ENDED
    
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

#     def _skip_digits(self):
#         while self._has_symbols_left():
#             if self._peek_symbol().isdigit():
#                 self.symbol_index += 1
#             else:
#                 break

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
