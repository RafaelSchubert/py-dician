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
        return self._rollexpr()

    def _rollexpr(self):
        return self._arithmeticexpr()

    def _arithmeticexpr(self):
        return self._sumorsubexpr()

    def _sumorsubexpr(self):
        if self._prodordivexpr():
            return self._sumorsubrighthandexpr()
        return False

    def _sumorsubrighthandexpr(self):
        if not self._plusorminusexpr():
            return True
        if not self._prodordivexpr():
            raise UnexpectedTokenError(self._token)
        return self._sumorsubrighthandexpr()

    def _plusorminusexpr(self):
        return self._consumeanyof(lexic.TokenType.SB_PLUS, lexic.TokenType.SB_MINUS)

    def _prodordivexpr(self):
        if self._signaledvalueexpr():
            return self._prodordivrighthandexpr()
        return False

    def _prodordivrighthandexpr(self):
        if not self._multordivexpr():
            return True
        if not self._signaledvalueexpr():
            raise UnexpectedTokenError(self._token)
        return self._prodordivrighthandexpr()

    def _multordivexpr(self):
        return self._consumeanyof(lexic.TokenType.SB_MULTIPLY, lexic.TokenType.SB_DIVIDE)

    def _signaledvalueexpr(self):
        if not self._plusorminusexpr():
            return self._valueexpr()
        if self._valueexpr():
            return True
        raise UnexpectedTokenError(self._token)

    def _valueexpr(self):
        return self._dicesetexpr()

    def _dicesetexpr(self):
        if self._numberexpr():
            return self._dicesetrighthandexpr()
        return False

    def _dicesetrighthandexpr(self):
        self._dieexpr()
        return True

    def _numberexpr(self):
        if self._parenthesizedexpr():
            return True
        if self._dieexpr():
            return True
        return self._integerexpr()

    def _parenthesizedexpr(self):
        if not self._leftparenthesisexpr():
            return False
        if not self._arithmeticexpr():
            raise UnexpectedTokenError(self._token)
        if self._rightparenthesisexpr():
            return True
        raise UnexpectedTokenError(self._token)

    def _leftparenthesisexpr(self):
        return self._consumeanyof(lexic.TokenType.SB_LPARENTHESIS)

    def _rightparenthesisexpr(self):
        return self._consumeanyof(lexic.TokenType.SB_RPARENTHESIS)

    def _dieexpr(self):
        if not self._dietagexpr():
            return False
        if self._numberexpr():
            return True
        raise UnexpectedTokenError(self._token)

    def _dietagexpr(self):
        return self._consumeanyof(lexic.TokenType.KW_D)

    def _integerexpr(self):
        return self._consumeanyof(lexic.TokenType.INTEGER)

    def _consumeanyof(self, *expected_token_types):
        if not self._token.kind in expected_token_types:
            return False
        self._nexttoken()
        return True

    def _nexttoken(self):
        self._token = self._tokenizer.fetch()

if __name__ == '__main__':
    expression = '3 * +1 / 2d6 - 2 + 1dd6 / -(2 + 1)d10 - 5 + +d4d8 * dd3dd12'
    my_parser  = Parser()
    print(f'Is "{expression}" a valid roll expression?')
    try:
        print('Yes.' if my_parser.parse(expression) else 'No.')
    except (lexic.TokenizerError, ParserError) as e:
        print(f'Nope. Something went wrong!')
        print(f'--> {e}')