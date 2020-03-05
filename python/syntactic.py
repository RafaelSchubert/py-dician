import lexic

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
        return self._sumorsubexpr()

    def _sumorsubexpr(self):
        if self._dicecomboexpr():
            return self._sumorsubrighthandexpr()

        return False

    def _dicecomboexpr(self):
        if self._token.kind != lexic.TokenType.INTEGER:
            return False

        self._nexttoken()

        return self._dicecomborighthandexpr()

    def _dicecomborighthandexpr(self):
        if self._token.kind == lexic.TokenType.END:
            return True

        if self._tokenisplusorminus():
            return True

        return self._diceexpr()

    def _diceexpr(self):
        if self._token.kind != lexic.TokenType.KW_D:
            return False

        self._nexttoken()

        if self._token.kind != lexic.TokenType.INTEGER:
            return False

        self._nexttoken()

        return True

    def _sumorsubrighthandexpr(self):
        if self._token.kind == lexic.TokenType.END:
            return True

        if self._plusorminusexpr():
            return self._sumorsubexpr()

        return False

    def _plusorminusexpr(self):
        if self._tokenisplusorminus():
            self._nexttoken()

            return True

        return False

    def _tokenisplusorminus(self):
        if self._token.kind == lexic.TokenType.SB_PLUS:
            return True

        if self._token.kind == lexic.TokenType.SB_MINUS:
            return True

        return False

    def _nexttoken(self):
        self._token = self._tokenizer.fetch()

if __name__ == '__main__':
    expression = '1d6 + 1d6'
    my_parser  = Parser()

    print(f'Is "{expression}" a valid roll expression?')

    try:
        print('Yes.' if my_parser.parse(expression) else 'No.')
    except lexic.TokenizerError as e:
        print(f'Nope. Something went wrong!')
        print(f'--> {e}')