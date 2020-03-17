import lexic


class ParserError(Exception):
    pass


class UnexpectedTokenError(ParserError):
    def __init__(self, found_token, expected_token_type=None):
        self.found_token = found_token
        self.expected_token_type = expected_token_type

    def __repr__(self):
        return f'{self.__class__.__name__}(found_token="{self.found_token}", expected_token_type={self.expected_token_type})'

    def __str__(self):
        message = f'Ln {self.found_token.line}, Col {self.found_token.column}: "{self.found_token}": unexpected token.'

        if self.expected_token_type == None:
            return message

        return message + f' Expected = {self.expected_token_type}.'


class Parser():
    def __init__(self):
        self._tokenizer = lexic.Tokenizer()
        self._current_token = None

    def parse(self, input_string):
        self._tokenizer.set_input_string(input_string)

        self._next_token()

        if not self._roll_expression():
            return False

        if self._expect_token_is_any_of(lexic.TokenType.END):
            return True

        self._raise_unexpected_token_error(lexic.TokenType.END)

    def _roll_expression(self):
        return self._arithmetic_expression()

    def _arithmetic_expression(self):
        return self._addition_or_subtraction()

    def _addition_or_subtraction(self):
        if self._product_or_division():
            return self._addition_or_subtraction_right_hand()

        return False

    def _addition_or_subtraction_right_hand(self):
        if not self._plus_or_minus():
            return True

        if not self._product_or_division():
            self._raise_unexpected_token_error()

        return self._addition_or_subtraction_right_hand()

    def _plus_or_minus(self):
        return self._expect_token_is_any_of(lexic.TokenType.PLUS, lexic.TokenType.MINUS)

    def _product_or_division(self):
        if self._signaled_value():
            return self._product_or_division_right_hand()

        return False

    def _product_or_division_right_hand(self):
        if not self._multiply_or_divide():
            return True

        if not self._signaled_value():
            self._raise_unexpected_token_error()

        return self._product_or_division_right_hand()

    def _multiply_or_divide(self):
        return self._expect_token_is_any_of(lexic.TokenType.MULTIPLY, lexic.TokenType.DIVIDE)

    def _signaled_value(self):
        if not self._plus_or_minus():
            return self._value_expression()

        if self._value_expression():
            return True

        self._raise_unexpected_token_error()

    def _value_expression(self):
        return self._dice_set_expression()

    def _dice_set_expression(self):
        if self._number_expression():
            return self._dice_set_expression_right_hand()

        return False

    def _dice_set_expression_right_hand(self):
        self._die_expression()
        return True

    def _number_expression(self):
        if self._parenthesized_expression():
            return True

        if self._die_expression():
            return True

        return self._expect_token_is_any_of(lexic.TokenType.INTEGER)

    def _parenthesized_expression(self):
        if not self._expect_token_is_any_of(lexic.TokenType.LEFT_PARENTHESIS):
            return False

        if not self._arithmetic_expression():
            self._raise_unexpected_token_error()

        if self._expect_token_is_any_of(lexic.TokenType.RIGHT_PARENTHESIS):
            return True

        self._raise_unexpected_token_error(lexic.TokenType.RIGHT_PARENTHESIS)

    def _die_expression(self):
        if not self._expect_token_is_any_of(lexic.TokenType.DIE):
            return False

        if self._number_expression():
            return True

        self._raise_unexpected_token_error()

    def _expect_token_is_any_of(self, *expected_token_types):
        return self._expect_token_is(lambda token: token.kind in expected_token_types)

    def _expect_token_is(self, condition):
        if not condition(self._current_token):
            return False

        self._next_token()

        return True

    def _next_token(self):
        self._current_token = self._tokenizer.next_token()

    def _raise_unexpected_token_error(self, expected_token_type=None):
        raise UnexpectedTokenError(self._current_token, expected_token_type)


if __name__ == '__main__':
    expression = '3 * +1 / 2d6 - 2 + 1dd6 / -(2 + 1)d10 - 5 + +d4d8 * dd3dd12'
    my_parser  = Parser()
    print(f'Is "{expression}" a valid roll expression?')
    try:
        print('Yes.' if my_parser.parse(expression) else 'No.')
    except (lexic.TokenizerError, ParserError) as e:
        print(f'Nope. Something went wrong!')
        print(f'--> {e}')