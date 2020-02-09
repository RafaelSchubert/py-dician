from enum import Enum, unique, auto

@unique
class Tokens(Enum):
    KeyWord_d = auto()
    Literal_Integer = auto()
    Symbol_Plus = auto()
    Symbol_Minus = auto()
    Symbol_ParenthesisLeft = auto()
    Symbol_ParenthesisRight = auto()

class Tokenizer():
    def __init__(self, text):
        self.text = text
        self.symbol_index = 0
        self.token_start = 0

    def _has_symbols_left(self):
        return self.symbol_index < len(self.text)

    def _read_symbol(self):
        if self._has_symbols_left():
            symbol = self.text[self.symbol_index]
            self.symbol_index += 1
            return symbol
        return None
    
    def _peek_symbol(self):
        if self._has_symbols_left():
            return self.text[self.symbol_index]
        return None

    def _skip_blanks(self):
        while self._has_symbols_left():
            if self._peek_symbol().isspace():
                self.symbol_index += 1
            else:
                break

    def _skip_digits(self):
        while self._has_symbols_left():
            if self._peek_symbol().isdigit():
                self.symbol_index += 1
            else:
                break

    def _start_token(self):
        self.token_start = self.symbol_index

    def _token_string(self):
        return self.text[self.token_start:self.symbol_index]

    def _fetch_token(self, tk_type):
        token = (tk_type, (self.token_start, self.symbol_index), self._token_string())
        self._start_token()
        return token

    def next(self):
        self._skip_blanks()
        self._start_token()
        current = self._read_symbol()
        if not current is None:
            if current.casefold() == 'd':
                return self._fetch_token(Tokens.KeyWord_d)
            if current == '+':
                return self._fetch_token(Tokens.Symbol_Plus)
            if current == '-':
                return self._fetch_token(Tokens.Symbol_Minus)
            if current == '(':
                return self._fetch_token(Tokens.Symbol_ParenthesisLeft)
            if current == ')':
                return self._fetch_token(Tokens.Symbol_ParenthesisRight)
            if current.isdigit():
                self._skip_digits()
                return self._fetch_token(Tokens.Literal_Integer)
        return None

dice_expression = input('Input a dice combo: ')

tk_fetcher = Tokenizer(dice_expression)

tk = tk_fetcher.next()
while not tk is None:
    print(tk)
    tk = tk_fetcher.next()