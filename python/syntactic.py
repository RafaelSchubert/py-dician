import lexic

class ParserError(Exception):
    pass

class UnexpectedTokenError(ParserError):
    def __init__(self, found_token, expected_token_type = None):
        self.found_token         = found_token
        self.expected_token_type = expected_token_type

    def __str__(self):
        message = f'An unexpected token was found. Found = {self.found_token}.'
        if self.expected_token_type == None:
            return message
        return message + f' Expected = {self.expected_token_type}.'

class Parser():
    def __init__(self):
        self._tokenizer = lexic.Tokenizer()
        self._token     = None

    def parse(self, text):
        self._tokenizer.parse(text)
        self._nexttoken()
        if self._token.kind == lexic.TokenType.END:
            return True
        if self._rollexpr():
            return True
        raise UnexpectedTokenError(self._token)

    def _rollexpr(self):
        return self._sumorsubexpr()

    def _sumorsubexpr(self):
        if self._prodordivexpr():
            return self._sumorsubrighthandexpr()
        return False

    def _prodordivexpr(self):
        if self._diceorintegerexpr():
            return self._prodordivrighthandexpr()
        return False

    def _diceorintegerexpr(self):
        if self._token.kind == lexic.TokenType.INTEGER:
            self._nexttoken()
            return self._optionaldieexpr()
        return self._dieexpr()

    def _optionaldieexpr(self):
        if self._token.kind == lexic.TokenType.KW_D:
            self._nexttoken()
            return self._diefaceexpr()
        return True

    def _dieexpr(self):
        if self._token.kind == lexic.TokenType.KW_D:
            self._nexttoken()
            return self._diefaceexpr()
        raise UnexpectedTokenError(self._token, lexic.TokenType.KW_D)

    def _diefaceexpr(self):
        if self._token.kind == lexic.TokenType.INTEGER:
            self._nexttoken()
            return True
        raise UnexpectedTokenError(self._token, lexic.TokenType.INTEGER)

    def _prodordivrighthandexpr(self):
        if self._multordivexpr():
            self._diceorintegerexpr()
            return self._prodordivrighthandexpr()
        return True

    def _sumorsubrighthandexpr(self):
        if self._plusorminusexpr():
            self._prodordivexpr()
            return self._sumorsubrighthandexpr()
        return True

    def _plusorminusexpr(self):
        if self._tokenisplusorminus():
            self._nexttoken()
            return True
        return False

    def _multordivexpr(self):
        if self._tokenismultordiv():
            self._nexttoken()
            return True
        return False

    def _tokenisplusorminus(self):
        if self._token.kind == lexic.TokenType.SB_PLUS:
            return True
        if self._token.kind == lexic.TokenType.SB_MINUS:
            return True
        return False

    def _tokenismultordiv(self):
        if self._token.kind == lexic.TokenType.SB_MULTIPLY:
            return True
        if self._token.kind == lexic.TokenType.SB_DIVIDE:
            return True
        return False

    def _nexttoken(self):
        self._token = self._tokenizer.fetch()

if __name__ == '__main__':
    expression = '3 * 1 / 2d6 - 2 + 1d6 / 3d10 - 5'
    my_parser  = Parser()
    print(f'Is "{expression}" a valid roll expression?')
    try:
        print('Yes.' if my_parser.parse(expression) else 'No.')
    except (lexic.TokenizerError, ParserError) as e:
        print(f'Nope. Something went wrong!')
        print(f'--> {e}')