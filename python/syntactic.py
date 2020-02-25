import lexic

class Parser():
    def __init__(self):
        self._tokenizer = lexic.Tokenizer()

    def parse(self, text):
        self._tokenizer.parse(text)

        self._rollexpr()

    def _rollexpr(self):
        self._sumorsubexpr()

    def _sumorsubexpr(self):
        self._dicecomboexpr()
        self._optionalsumorsubrighthandexpr()

    def _dicecomboexpr(self):
        self._optionaldiceexpr()

    def _optionaldiceexpr(self):
        self._diceexpr()

    def _diceexpr(self):
        pass

    def _optionalsumorsubrighthandexpr(self):
        self._plusorminusexpr()
        self._sumorsubexpr()

    def _plusorminusexpr(self):
        pass

if __name__ == '__main__':
    my_parser = Parser()
    # my_parser.parse('2d10')