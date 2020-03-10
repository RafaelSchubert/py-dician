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
        if self._diceorintegerexpr():
            return self._sumorsubrighthandexpr()
        return False

    def _diceorintegerexpr(self):
        if self._token.kind == lexic.TokenType.INTEGER:
            self._nexttoken()
            return self._optionaldieexpr()
        raise UnexpectedTokenError(self._token, lexic.TokenType.INTEGER)

    def _optionaldieexpr(self):
        if self._token.kind == lexic.TokenType.KW_D:
            self._nexttoken()
            return self._diefaceexpr()
        return True

    def _diefaceexpr(self):
        if self._token.kind == lexic.TokenType.INTEGER:
            self._nexttoken()
            return True
        raise UnexpectedTokenError(self._token, lexic.TokenType.INTEGER)

    def _sumorsubrighthandexpr(self):
        if self._token.kind == lexic.TokenType.SB_PLUS or self._token.kind == lexic.TokenType.SB_MINUS:
            self._nexttoken()
            return self._sumorsubexpr()
        return True

    def _nexttoken(self):
        self._token = self._tokenizer.fetch()

if __name__ == '__main__':
    expression = '3 + 1 + 2d6 - 2 + 1d6 + 3d10 - 5'
    my_parser  = Parser()

    print(f'Is "{expression}" a valid roll expression?')

    try:
        print('Yes.' if my_parser.parse(expression) else 'No.')
    except (lexic.TokenizerError, ParserError) as e:
        print(f'Nope. Something went wrong!')
        print(f'--> {e}')