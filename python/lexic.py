from enum import Enum, auto

SYMBOL_LEFT_PARENTHESIS  = '('
SYMBOL_RIGHT_PARENTHESIS = ')'
SYMBOL_PLUS              = '+'
SYMBOL_MINUS             = '-'
SYMBOL_MULTIPLY          = '*'
SYMBOL_DIVIDE            = '/'
KEYWORD_D                = 'd'

class TokenType(Enum):
    END             = auto()
    SB_LPARENTHESIS = auto()
    SB_RPARENTHESIS = auto()
    SB_PLUS         = auto()
    SB_MINUS        = auto()
    SB_MULTIPLY     = auto()
    SB_DIVIDE       = auto()
    INTEGER         = auto()
    KW_D            = auto()

    def isend(self):
        return self == TokenType.END

    def issymbol(self):
        if self == TokenType.SB_LPARENTHESIS:
            return True
        if self == TokenType.SB_RPARENTHESIS:
            return True
        if self == TokenType.SB_PLUS:
            return True
        if self == TokenType.SB_MINUS:
            return True
        if self == TokenType.SB_MULTIPLY:
            return True
        if self == TokenType.SB_DIVIDE:
            return True
        return False

    def iskeyword(self):
        return self == TokenType.KW_D
    
    def isliteral(self):
        return self == TokenType.INTEGER

    def __str__(self):
        if self == TokenType.END:
            return 'End'
        if self == TokenType.SB_LPARENTHESIS:
            return 'Left Parethesis'
        if self == TokenType.SB_RPARENTHESIS:
            return 'Right Parethesis'
        if self == TokenType.SB_PLUS:
            return 'Plus'
        if self == TokenType.SB_MINUS:
            return 'Minus'
        if self == TokenType.SB_MULTIPLY:
            return 'Multiply'
        if self == TokenType.SB_DIVIDE:
            return 'Divide'
        if self == TokenType.KW_D:
            return 'Dice'
        if self == TokenType.INTEGER:
            return 'Integer'
        return 'None'

class Token():
    def __init__(self, kind, value, line, column):
        self.kind   = kind
        self.value  = value
        self.line   = line
        self.column = column

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
        self._text           = text
        self._current_index  = 0
        self._current_line   = 1
        self._current_column = 1
        self._token_start    = self._current_index
        self._token_line     = self._current_line
        self._token_column   = self._current_column

    def fetch(self):
        self._skipblanks()
        self._begintoken()
        try:
            current = self._peek()
        except EndOfTextError:
            return self._extracttoken(TokenType.END)
        if self._checkislparenthesis(current):
            return self._getlparenthesis()
        if self._checkisrparenthesis(current):
            return self._getrparenthesis()
        if self._checkisplus(current):
            return self._getplus()
        if self._checkisminus(current):
            return self._getminus()
        if self._checkismultiply(current):
            return self._getmultiply()
        if self._checkisdivide(current):
            return self._getdivide()
        if self._checkiskeywordd(current):
            return self._getdice()
        if current.isdigit():
            return self._readinteger()
        self._next      ()
        self._begintoken()
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

    def _next(self):
        if self._peek() == '\n':
            self._current_line   += 1
            self._current_column  = 1
        else:
            self._current_column += 1
        self._current_index += 1

    def _begintoken(self):
        self._token_start  = self._current_index
        self._token_line   = self._current_line
        self._token_column = self._current_column

    def _skipwhile(self, condition):
        while self._hassymbolsleft():
            if condition(self._peek()):
                self._next()
            else:
                break

    def _skipblanks(self):
        self._skipwhile(lambda x: x.isspace())

    def _skipdigits(self):
        self._skipwhile(lambda x: x.isdigit())

    def _tokenstring(self):
        return self._text[self._token_start:self._current_index]

    def _extracttoken(self, kind):
        token = Token(kind, self._tokenstring(), self._token_line, self._token_column)
        self._begintoken()
        return token

    def _getlparenthesis(self):
        return self._extracttoken(TokenType.SB_LPARENTHESIS)

    def _getrparenthesis(self):
        return self._extracttoken(TokenType.SB_RPARENTHESIS)

    def _getplus(self):
        return self._extracttoken(TokenType.SB_PLUS)

    def _getminus(self):
        return self._extracttoken(TokenType.SB_MINUS)

    def _getmultiply(self):
        return self._extracttoken(TokenType.SB_MULTIPLY)

    def _getdivide(self):
        return self._extracttoken(TokenType.SB_DIVIDE)

    def _getinteger(self):
        return self._extracttoken(TokenType.INTEGER)

    def _getdice(self):
        return self._extracttoken(TokenType.KW_D)

    def _checkislparenthesis(self, token):
        return self._consumeifisanyof(token, SYMBOL_LEFT_PARENTHESIS)

    def _checkisrparenthesis(self, token):
        return self._consumeifisanyof(token, SYMBOL_RIGHT_PARENTHESIS)

    def _checkisplus(self, token):
        return self._consumeifisanyof(token, SYMBOL_PLUS)

    def _checkisminus(self, token):
        return self._consumeifisanyof(token, SYMBOL_MINUS)

    def _checkismultiply(self, token):
        return self._consumeifisanyof(token, SYMBOL_MULTIPLY)

    def _checkisdivide(self, token):
        return self._consumeifisanyof(token, SYMBOL_DIVIDE)

    def _checkiskeywordd(self, token):
        return self._consumeifisanyof(token.casefold(), KEYWORD_D)

    def _consumeifisanyof(self, symbol, *expected_symbols):
        if not symbol in expected_symbols:
            return False
        self._next()
        return True

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
