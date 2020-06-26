from typing import Callable, Tuple
from error import ParseError
from lexic import Closure, EndOfStringError, Token, Tokenizer, TokenType
from optree import DiceRollOp, DieOp, DivideOp, LiteralValueOp, MultiplyOp, NegateOp, Operation, SubtractOp, SumOp


class UnexpectedTokenError(ParseError):
    """Exception thrown by the Parser class when a token of a type unexpected by the syntax is found.

    Parameters:
        found_token (Token): the token that was found.
    """

    def __init__(self, found_token: Token):
        super().__init__(found_token.line, found_token.column)
        self.found_token = found_token


class ClosureError(ParseError):
    """Exception thrown by the Parser class when an error related to an enclosed expression happens.

    Parameters:
        closure (Closure): the type of closure.
        line (int): the line at which the error was noticed.
        column (int): the position in the line at which the error was noticed.
    """

    def __init__(self, closure: Closure, line: int, column: int):
        super().__init__(line, column)
        self.closure = closure


class OrphanClosureBeginError(ClosureError):
    """Exception thrown by the Parser class when there's an enclosed expression left open.

    Parameters:
        closure (Closure): the type of closure that was left open.
        line (int): the line at which the enclosed expression begins.
        column (int): the position in the line at which the enclosed expression begins.
    """

    pass


class OrphanClosureEndError(ClosureError):
    """Exception thrown by the Parser class when there's a closure's end with no matching begin.

    Parameters:
        closure (Closure): the type of the unopened closure.
        line (int): the line at which the closure's end was found.
        column (int): the position in the line at which the closure's end was found.
    """

    pass


class IncompleteEnclosedExpressionError(ClosureError):
    """Exception thrown by the Parser class when there's an incomplete enclosed expression.

    Parameters:
        closure (Closure): the type of closure.
        line (int): the line at which the enclosed expression begins.
        column (int): the position in the line at which the enclosed expression begins.
    """

    pass


class Parser():
    """Class that parses a string accordingly to the dice-language, checking its syntactical and semantical validity."""

    def __init__(self):
        self._tokenizer = Tokenizer()

    def parse(self, input_string: str) -> Operation:
        """Parses and validates a string accordingly to the dice-language.

        Parameters:
            input_string (str): the string to be parsed.

        Returns:
            True if the string is valid. False, otherwise.

        Raises:
            UnexpectedTokenError if a token of an unexpected type is found at any moment.
        """

        self._ready(input_string)

        roll_op = self._roll_expression()

        if self._current_token.kind is TokenType.END:
            return roll_op

        self._handle_unexpected_token()

    def _ready(self, input_string: str) -> None:
        self._tokenizer.set_input_string(input_string)
        self._reset_diagnostic()
        self._next_token()

    def _reset_diagnostic(self) -> None:
        self._closure_stack = []

    def _roll_expression(self) -> Operation:
        # Tries to parse a roll expression, starting at the current token.

        return self._addition_or_subtraction()

    def _addition_or_subtraction(self) -> Operation:
        # Tries to parse an addition or a subtraction, starting at the current token.

        left_operand = self._product_or_division()

        if left_operand is None:
            return None

        return self._addition_or_subtraction_right_hand(left_operand)

    def _addition_or_subtraction_right_hand(self, left_operand: Operation) -> Operation:
        # Tries to parse the optional right side of an addition or a subtraction, starting at the current token.

        op_token_type = self._current_token.kind

        if not op_token_type in (TokenType.PLUS, TokenType.MINUS):
            return left_operand

        self._next_token()

        right_operand = self._product_or_division()

        if right_operand is None:
            self._handle_unexpected_token()

        operation = None

        if op_token_type is TokenType.PLUS:
            operation = SumOp(left_operand, right_operand)
        else:
            operation = SubtractOp(left_operand, right_operand)

        return self._addition_or_subtraction_right_hand(operation)

    def _product_or_division(self) -> Operation:
        # Tries to parse a multiplication or a division, starting at the current token.

        left_operand = self._positive_or_negative()

        if left_operand is None:
            return None

        return self._product_or_division_right_hand(left_operand)

    def _product_or_division_right_hand(self, left_operand: Operation) -> Operation:
        # Tries to parse the optional right side of a multiplication or a division, starting at the current token.

        op_token_type = self._current_token.kind

        if not op_token_type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            return left_operand

        self._next_token()

        right_operand = self._positive_or_negative()

        if right_operand is None:
            self._handle_unexpected_token()

        operation = None

        if op_token_type is TokenType.MULTIPLY:
            operation = MultiplyOp(left_operand, right_operand)
        else:
            operation = DivideOp(left_operand, right_operand)

        return self._product_or_division_right_hand(operation)

    def _positive_or_negative(self) -> Operation:
        # Tries to parse a positive or a negative value, starting at the current token.

        op_token_type = self._current_token.kind

        if not op_token_type in (TokenType.PLUS, TokenType.MINUS):
            return self._dice_set_or_value()

        self._next_token()

        dice_val_op = self._dice_set_or_value()

        if dice_val_op is None:
            self._handle_unexpected_token()

        if op_token_type is TokenType.MINUS:
            return NegateOp(dice_val_op)

        return dice_val_op

    def _dice_set_or_value(self) -> Operation:
        # Tries to parse a dice set or a value, starting at the current token.

        value_op = self._value_expression()
        die_op = self._die_expression()

        if value_op is None:
            return die_op

        if die_op is None:
            return value_op

        return DiceRollOp(value_op, die_op)

    def _die_expression(self) -> Operation:
        # Tries to parse a die definition, starting at the current token.

        if not self._current_token.kind is TokenType.DIE:
            return None

        self._next_token()

        die_maximum_op = self._value_expression()

        if die_maximum_op is None:
            self._handle_unexpected_token()

        return DieOp(die_maximum_op)

    def _value_expression(self) -> Operation:
        # Tries to parse a value, starting at the current token.

        value_op = self._parenthesized_expression()

        if value_op is None:
            value_op = self._literal_expression()

        return value_op

    def _parenthesized_expression(self) -> Operation:
        # Tries to parse an expression enclosed by parentheses, starting at the current token.

        if not self._begin_closure(Closure.PARENTHESES):
            return None

        roll_op = self._roll_expression()

        if roll_op is None:
            self._handle_unexpected_token()

        if self._end_closure(Closure.PARENTHESES):
            return roll_op

        self._handle_unexpected_token()

    def _literal_expression(self) -> Operation:
        # Tries to parse a literal value expression, starting at the current token.

        return self._numeric_literal()

    def _numeric_literal(self) -> Operation:
        # Tries to parse a numeric literal value expression, starting at the current token.

        if not self._current_token.kind is TokenType.INTEGER:
            return None

        literal_op = LiteralValueOp(int(self._current_token.value))

        self._next_token()

        return literal_op

    def _expect_token_is_any_of(self, *expected_token_types: Tuple[TokenType, ...]) -> bool:
        # Checks if the current token is of any of the given types. If so, advances to next token.

        return self._expect_token_is(lambda token: token.kind in expected_token_types)

    def _expect_token_is(self, condition: Callable[[Token], bool]) -> bool:
        # Checks if the current token satisfies a given condition. If so, advances to next token.

        if not condition(self._current_token):
            return False

        self._next_token()

        return True

    def _next_token(self) -> None:
        self._current_token = self._tokenizer.next_token()

    def _begin_closure(self, closure: Closure) -> bool:
        current = self._current_token

        if not self._expect_token_is_any_of(closure.begin.token_type):
            return False

        self._closure_stack.append((closure, current))

        return True

    def _end_closure(self, expected_closure: Closure) -> bool:
        current = self._current_token

        if not self._expect_token_is_any_of(expected_closure.end.token_type):
            return False

        try:
            opened_closure = self._closure_stack.pop()

            if opened_closure[0] != expected_closure:
                raise OrphanClosureBeginError(opened_closure[0], opened_closure[1].line, opened_closure[1].column)
        except IndexError:
            # It seems that, if this one is ever raised, it'll be most likely an error in the parsing process.
            raise OrphanClosureEndError(expected_closure, current.line, current.column)

        return True

    def _handle_unexpected_token(self) -> None:
        if self._current_token.kind is TokenType.END:
            self._check_orphan_closure_begin()

            raise EndOfStringError(self._current_token.line, self._current_token.column)

        self._check_incomplete_enclosed_expression()

        raise UnexpectedTokenError(self._current_token)

    def _check_orphan_closure_begin(self) -> None:
        try:
            orphan_closure = self._closure_stack.pop()

            raise OrphanClosureBeginError(orphan_closure[0], orphan_closure[1].line, orphan_closure[1].column)
        except IndexError:
            pass

    def _check_incomplete_enclosed_expression(self) -> None:
        ended_closure = next((c for c in Closure if c.end.token_type==self._current_token.kind), None)

        if ended_closure is None:
            return

        try:
            opened_closure = self._closure_stack.pop()

            if opened_closure[0] is ended_closure:
                raise IncompleteEnclosedExpressionError(opened_closure[0], opened_closure[1].line, opened_closure[1].column)

            self._closure_stack.append(opened_closure)
        except IndexError:
            pass


if __name__ == '__main__':
    expression = '3 * +1 / 2d6 - 2 + 1d(d6) / -(2 + 1)d10 - 5 + +(d4)d8 * (d(d3))d(d12) + (d(4 + 2))d(6d6)'
    my_parser  = Parser()
    print(f'Is "{expression}" a valid roll expression?')
    try:
        roll_op_tree = my_parser.parse(expression)
        print('No.' if roll_op_tree is None else 'Yes.')
    except EndOfStringError as e:
        print(f'Ln {e.line}, Col {e.column}: The end of the string was reached.')
    except UnexpectedTokenError as e:
        print(f'Ln {e.line}, Col {e.column}: Unexpected token found: "{e.found_token}".')
    except OrphanClosureBeginError as e:
        print(f'Ln {e.line}, Col {e.column}: Orphan closure begin: "{e.closure.begin}" - no matching "{e.closure.end}" found.')
    except OrphanClosureEndError as e:
        print(f'Ln {e.line}, Col {e.column}: Orphan closure end: "{e.closure.end}" - no matching "{e.closure.begin}" found previously.')
    except IncompleteEnclosedExpressionError as e:
        print(f'Ln {e.line}, Col {e.column}: Incomplete enclosed expression: the expression enclosed by "{e.closure.begin} {e.closure.end}" is possibly incomplete.')
    except ParseError as e:
        print(f'Something went wrong! --> {repr(e)}')
