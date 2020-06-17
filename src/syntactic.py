from typing import Callable, Tuple
from lexic import Token, Tokenizer, TokenizerError, TokenType


class ParserError(Exception):
    """Base-class for the Parser class' exceptions."""

    pass


class UnexpectedTokenError(ParserError):
    """
    Exception thrown by the Parser class when a token of an unexpected type is found.

    Parameters:
        found_token (Token): the token that was found.
        [optional] expected_token_type (TokenType): the token type that was expected to be found instead.
    """

    def __init__(self, found_token: Token, expected_token_type: TokenType = None):
        self.found_token = found_token
        self.expected_token_type = expected_token_type

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(found_token="{self.found_token}", expected_token_type={self.expected_token_type})'

    def __str__(self) -> str:
        message = f'Ln {self.found_token.line}, Col {self.found_token.column}: "{self.found_token}": unexpected token.'

        if self.expected_token_type == None:
            return message

        return message + f' Expected = {self.expected_token_type}.'


class Parser():
    """Class that parses a string accordingly to the dice-language, checking its syntactical and semantical validity."""

    def __init__(self):
        self._tokenizer = Tokenizer()
        self._current_token = None

    def parse(self, input_string: str) -> bool:
        """
        Parses and validates a string accordingly to the dice-language.

        Parameters:
            input_string (str): the string to be parsed.

        Returns:
            True if the string is valid. False, otherwise.

        Raises:
            UnexpectedTokenError if a token of an unexpected type is found at any moment.
        """

        self._tokenizer.set_input_string(input_string)

        self._next_token()

        if not self._roll_expression():
            return False

        if self._expect_token_is_any_of(TokenType.END):
            return True

        self._raise_unexpected_token_error(TokenType.END)

    def _roll_expression(self) -> bool:
        return self._expression()

    def _expression(self) -> bool:
        return self._arithmetic_expression()

    def _arithmetic_expression(self) -> bool:
        return self._addition_or_subtraction()

    def _addition_or_subtraction(self) -> bool:
        if self._product_or_division():
            return self._addition_or_subtraction_right_hand()

        return False

    def _addition_or_subtraction_right_hand(self) -> bool:
        if not self._plus_or_minus():
            return True

        if not self._product_or_division():
            self._raise_unexpected_token_error()

        return self._addition_or_subtraction_right_hand()

    def _plus_or_minus(self) -> bool:
        return self._expect_token_is_any_of(TokenType.PLUS, TokenType.MINUS)

    def _product_or_division(self) -> bool:
        if self._positive_or_negative():
            return self._product_or_division_right_hand()

        return False

    def _product_or_division_right_hand(self) -> bool:
        if not self._multiply_or_divide():
            return True

        if not self._positive_or_negative():
            self._raise_unexpected_token_error()

        return self._product_or_division_right_hand()

    def _multiply_or_divide(self) -> bool:
        return self._expect_token_is_any_of(TokenType.MULTIPLY, TokenType.DIVIDE)

    def _positive_or_negative(self) -> bool:
        if not self._plus_or_minus():
            return self._dice_set_or_value()

        if self._dice_set_or_value():
            return True

        self._raise_unexpected_token_error()

    def _dice_set_or_value(self) -> bool:
        if self._value_expression():
            return self._optional_die()

        return self._die_expression()

    def _optional_die(self) -> bool:
        self._die_expression()

        return True

    def _die_expression(self) -> bool:
        if not self._expect_token_is_any_of(TokenType.DIE):
            return False

        if self._value_expression():
            return True

        self._raise_unexpected_token_error()

    def _value_expression(self) -> bool:
        if self._parenthesized_expression():
            return True

        return self._literal_expression()

    def _parenthesized_expression(self) -> bool:
        if not self._expect_token_is_any_of(TokenType.LEFT_PARENTHESIS):
            return False

        if not self._expression():
            self._raise_unexpected_token_error()

        if self._expect_token_is_any_of(TokenType.RIGHT_PARENTHESIS):
            return True

        self._raise_unexpected_token_error(TokenType.RIGHT_PARENTHESIS)

    def _literal_expression(self) -> bool:
        return self._numeric_literal()

    def _numeric_literal(self) -> bool:
        return self._expect_token_is_any_of(TokenType.INTEGER)

    def _expect_token_is_any_of(self, *expected_token_types: Tuple[TokenType, ...]) -> bool:
        return self._expect_token_is(lambda token: token.kind in expected_token_types)

    def _expect_token_is(self, condition: Callable[[Token], bool]) -> bool:
        if not condition(self._current_token):
            return False

        self._next_token()

        return True

    def _next_token(self) -> None:
        self._current_token = self._tokenizer.next_token()

    def _raise_unexpected_token_error(self, expected_token_type: TokenType = None) -> None:
        raise UnexpectedTokenError(self._current_token, expected_token_type)


if __name__ == '__main__':
    expression = '3 * +1 / 2d6 - 2 + 1d(d6) / -(2 + 1)d10 - 5 + +(d4)d8 * (d(d3))d(d12) + (d(4 + 2))d(6d6)'
    my_parser  = Parser()
    print(f'Is "{expression}" a valid roll expression?')
    try:
        print('Yes.' if my_parser.parse(expression) else 'No.')
    except (TokenizerError, ParserError) as e:
        print(f'Nope. Something went wrong!')
        print(f'--> {e}')