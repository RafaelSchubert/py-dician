from typing import Any, Callable, NamedTuple, Tuple
from enum import Enum, unique
from random import randint


class PyDicianError(Exception):
    """Base-class for Py-Dician errors."""

    pass


class OperationError(PyDicianError):
    """Base-class for operation-related errors."""

    pass


class Operation:
    """Base-class of the executable operations to which Py-Dician expressions are translated.

    An operation takes zero or more operands, which act as its parameters. Each operand should
    also be an operation that results in a value of a type accepted by the main operation.
    """

    def run(self) -> Any:
        """Executes this operation.

        Must be overridden by derived classes.

        Returns:
            The result of the operation, which could be anything really.
        """

        raise NotImplementedError


class SimpleOp(Operation):
    """Base-class of operations that take no operands (parameters), such as literal values."""

    pass


class UnaryOp(Operation):
    """Base-class of operations that take a single operand (parameter), such as arithmetic-negation or die definition.

    Parameters:
        operand (Operation): the single operand of this operation.
    """

    def __init__(self, operand: Operation):
        super().__init__()
        self._operand = operand


class BinaryOp(Operation):
    """Base-class of operations that take exactly two operands (parameters) -- a left and a right one.

    Parameters:
        left_operand (Operation): the left operand of this operation.
        right_operand (Operation): the right operand of this operation.
    """

    def __init__(self, left_operand: Operation, right_operand: Operation):
        super().__init__()
        self._left_operand = left_operand
        self._right_operand = right_operand


class LiteralValueOp(SimpleOp):
    """Operation that produces a fixed, unmodified value.

    Parameters:
        value (Any): the value that'll be returned when the operaton is executed.
                     Note that a VALUE is expected, NOT an OPERATION.
    """

    def __init__(self, value: Any):
        super().__init__()
        self._value = value

    def run(self) -> Any:
        """Returns a fixed, unmodified value.

        Returns:
            The value that was stored at construction time, unmodified.
        """

        return self._value


class DieOp(UnaryOp):
    '''Operation that produces a "rollable die".

    In fact, the operation produces a callable that generates a random integer number in the range
    [1, n], with n being the result of the single operand of this operation.

    Parameters:
        operand (Operation): an operation that produces an integer number that'll be the maximum
                             value of the die.
    '''

    def run(self) -> Callable[[], int]:
        '''Returns a "rollable die" in the form of a callable.

        Returns:
            A parameterless callable that generates a random integer number in the range [1, n],
            with n being the maximum value of the die.
        '''

        die_maximum = int(self._operand.run())

        return lambda: randint(1, die_maximum)


class DiceRollOp(BinaryOp):
    """Operation that produces the sum of multiple rolls of a single die type.

    Parameters:
        left_operand (Operation): an operation that produces the number of rolled dice.
        right_operand (Operation): an operation that produces a die type.
    """

    def __init__(self, left_operand: Operation, right_operand: Operation):
        super().__init__(left_operand, right_operand)

    def run(self) -> int:
        """Returns the sum of multiple rolls of a single die.

        Returns:
            The sum of the results of multiple rolls of a single type of die.
        """

        dice_count = int(self._left_operand.run())
        die = self._right_operand.run()

        return sum(die() for i in range(dice_count))


class NegateOp(UnaryOp):
    """Operation that produces the arithmetic-negation of a value.

    Parameters:
        operand (Operation): an operation that produces the value to be arithmetically negated.
    """

    def run(self) -> Any:
        """Returns the arithmetic-negation of a value.

        Returns:
            The result of the expression -n, where n is the value produced the single operand of
            this operation.
        """

        return -self._operand.run()


class SumOp(BinaryOp):
    """Operation that produces the sum of two values.

    Parameters:
        left_operand (Operation): an operation that produces the left-side value of the sum.
        right_operand (Operation): an operation that produces the right-side value of the sum.
    """

    def run(self) -> int:
        """Returns the sum of two values.

        Returns:
            The result of the sum (a + b) of the two vales produced by the operands of this operation.
        """

        return self._left_operand.run() + self._right_operand.run()


class SubtractOp(BinaryOp):
    """Operation that produces the subtraction of two values.

    Parameters:
        left_operand (Operation): an operation that produces the left-side value of the subtraction.
        right_operand (Operation): an operation that produces the right-side value of the subtraction.
    """

    def run(self) -> int:
        """Returns the subtraction of two values.

        Returns:
            The result of the subtraction (a - b) of the two vales produced by the operands of this operation.
        """

        return self._left_operand.run() - self._right_operand.run()


class MultiplyOp(BinaryOp):
    """Operation that produces the multiplication of two values.

    Parameters:
        left_operand (Operation): an operation that produces the left-side value of the multiplication.
        right_operand (Operation): an operation that produces the right-side value of the multiplication.
    """

    def run(self) -> int:
        """Returns the multiplication of two values.

        Returns:
            The result of the multiplication (a * b) of the two vales produced by the operands of this operation.
        """

        return self._left_operand.run() * self._right_operand.run()


class DivideOp(BinaryOp):
    """Operation that produces the division of two values.

    Parameters:
        left_operand (Operation): an operation that produces the left-side value of the division.
        right_operand (Operation): an operation that produces the right-side value of the division.
    """

    def run(self) -> int:
        """Returns the division of two values.

        Returns:
            The result of the division (a / b) of the two vales produced by the operands of this operation.
        """

        return self._left_operand.run() / self._right_operand.run()


@unique
class TokenType(Enum):
    """Constants enumeration for Py-Dician's token types.

    Parameters:
        symbol (str): the symbol for that token type.
                      May be None if it's not represented by a symbol.
    """

    END = (None, )
    PLUS = ('+', )
    MINUS = ('-', )
    MULTIPLY = ('*', )
    DIVIDE = ('/', )
    LEFT_PARENTHESIS = ('(', )
    RIGHT_PARENTHESIS = (')', )
    DIE = ('d', )
    INTEGER = (None, )

    def __new__(cls, symbol: str):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__)
        obj.symbol = symbol
        return obj

    def __str__(self) -> str:
        return self.symbol if self.symbol else f'<{self.name}>'


@unique
class Closure(Enum):
    """Py-Dician's closures (pairs of tokens that enclose expressions).

    Parameters:
        begin (TokenType): the type of token that opens the closure.
        end (TokenType): the type of token that closes the closure.
    """

    PARENTHESES = (TokenType.LEFT_PARENTHESIS, TokenType.RIGHT_PARENTHESIS)

    def __new__(cls, begin: TokenType, end: TokenType):
        obj = object.__new__(cls)
        obj._value_ = len(cls.__members__)
        obj.begin = begin
        obj.end = end
        return obj

    def __str__(self) -> str:
        return str((str(self.begin), str(self.end)))


class Token():
    """Class that represents a Py-Dician token, extracted from a string.

    Parameters:
        type (TokenType): a member from the TokenType enum representing the token's type.
        value (str): the value of the token, extracted from the string.
        line (int): the line at which the token starts.
        column (int): the position in the line at which the token starts.
    """

    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return self.value if self.value else str(self.type)


class ParseError(PyDicianError):
    """Base-class for parse errors, either of lexical, syntactic or semantic nature.

    Parameters:
        line (int): the line at which the error occurred.
        column (int): the position in the line at which the error occurred.
    """

    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column


class EndOfStringError(ParseError):
    """Exception thrown by the Tokenizer class when the parse reaches the end of the parsed string.

    Parameters:
        line (int): the line at which the string ends.
        column (int): the position in the line at which the string ends.
    """

    pass


class UnknownSymbolError(ParseError):
    """Exception thrown by the Tokenizer class when it finds a symbol for which there's no defined token type.

    Parameters:
        symbol (str): the unknown symbol that was found.
        line (int): the line where the symbol was found.
        column (int): the position where the symbol was found in the line.
    """

    def __init__(self, symbol: str, line: int, column: int):
        super().__init__(line, column)
        self.symbol = symbol


class Tokenizer():
    """Class that parses a string accordingly to Py-Dician, fetching each token sequentially.

    Parameters:
        [optional] input_string (str): the string to be parsed. The default-value is an empty string, i.e. no string to parse.
    """

    def __init__(self, input_string: str = ''):
        self.set_input_string(input_string)

    def set_input_string(self, input_string: str) -> None:
        """Sets the string to be parsed and resets the parsing.

        Parameters:
            input_string (str): the string to be parsed.
        """

        self._input_string = input_string
        self.reset()

    def reset(self) -> None:
        """Resets the parsing to the beginning of the string."""

        self._current_symbol = self._input_string[0:1]
        self._current_index = 0
        self._current_line = 1
        self._current_column = 1
        self._begin_token()

    def next_token(self) -> Token:
        """Fetches the next token from the parsed string.

        Returns:
            A Token object containing the fetched token.
            If the end of the string is reached, an END (TokenType) token is returned.

        Raises:
            UnknownSymbolError if an unknown symbol is found.
        """

        try:
            self._skip_blanks()
            self._begin_token()

            if self._expect_symbol_is_any_of(TokenType.LEFT_PARENTHESIS):
                return self._fetch_token(TokenType.LEFT_PARENTHESIS)

            if self._expect_symbol_is_any_of(TokenType.RIGHT_PARENTHESIS):
                return self._fetch_token(TokenType.RIGHT_PARENTHESIS)

            if self._expect_symbol_is_any_of(TokenType.PLUS):
                return self._fetch_token(TokenType.PLUS)

            if self._expect_symbol_is_any_of(TokenType.MINUS):
                return self._fetch_token(TokenType.MINUS)

            if self._expect_symbol_is_any_of(TokenType.MULTIPLY):
                return self._fetch_token(TokenType.MULTIPLY)

            if self._expect_symbol_is_any_of(TokenType.DIVIDE):
                return self._fetch_token(TokenType.DIVIDE)

            if self._expect_symbol_is_any_of(TokenType.DIE):
                return self._fetch_token(TokenType.DIE)

            if self._expect_symbol_is_any_digit():
                return self._fetch_integer()

            self._raise_unknown_symbol_error()
        except EndOfStringError:
            return self._fetch_token(TokenType.END)

    def _raise_unknown_symbol_error(self) -> None:
        # Raises an UnknownSymbolError exception for the current symbol.

        unknown_symbol_error = UnknownSymbolError(self._current_symbol, self._current_line, self._current_column)

        self._next_symbol()
        self._begin_token()

        raise unknown_symbol_error

    def _fetch_integer(self) -> Token:
        # Fetches an INTEGER (TokenType) token, starting at the current symbol.

        self._skip_digits()
        return self._fetch_token(TokenType.INTEGER)

    def _has_symbols_left(self) -> bool:
        return self._current_index < len(self._input_string)

    def _next_symbol(self) -> None:
        # Advances the parsing to next character of the parsed string.

        if not self._has_symbols_left():
            raise EndOfStringError(self._current_line, self._current_column)

        self._current_index += 1
        if self._current_symbol == '\n':
            self._current_line += 1
            self._current_column  = 1
        else:
            self._current_column += 1

        self._current_symbol = self._input_string[self._current_index : self._current_index+1].casefold()

    def _begin_token(self) -> None:
        # Begins a new current token.

        self._token_start = self._current_index
        self._token_line = self._current_line
        self._token_column = self._current_column

    def _skip_symbols_while(self, condition: Callable[[str], bool]) -> None:
        # Skips symbols in the parsed string while they satisfy a given condition.

        while self._has_symbols_left():
            if condition(self._current_symbol):
                self._next_symbol()
            else:
                break

    def _skip_blanks(self) -> None:
        # Skips blanks (symbol.isspace() == True) in the parsed string.

        self._skip_symbols_while(lambda x: x.isspace())

    def _skip_digits(self) -> None:
        # Skips digits (symbol.isdigit() == True) in the parsed string.

        self._skip_symbols_while(lambda x: x.isdigit())

    def _fetch_token(self, token_type: TokenType) -> Token:
        # Returns the current token and begins a new one.

        token_value = self._input_string[self._token_start : self._current_index]
        token = Token(token_type, token_value, self._token_line, self._token_column)

        self._begin_token()

        return token

    def _expect_symbol_is_any_of(self, *expected_symbols: Tuple[TokenType, ...]) -> bool:
        # Checks if the current symbol is any of a given set. If it is, advances to the next symbol.

        if not self._current_symbol in (x.symbol for x in expected_symbols):
            return False

        self._next_symbol()

        return True

    def _expect_symbol_is_any_digit(self) -> bool:
        # Checks if the symbol a digit. If it is, advances to the next symbol.

        if not self._current_symbol.isdigit():
            return False

        self._next_symbol()

        return True


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

        if self._current_token.type is TokenType.END:
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

        op_token_type = self._current_token.type

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

        op_token_type = self._current_token.type

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

        op_token_type = self._current_token.type

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

        if not self._current_token.type is TokenType.DIE:
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

        if not self._current_token.type is TokenType.INTEGER:
            return None

        literal_op = LiteralValueOp(int(self._current_token.value))

        self._next_token()

        return literal_op

    def _next_token(self) -> None:
        self._current_token = self._tokenizer.next_token()

    def _begin_closure(self, closure: Closure) -> bool:
        current = self._current_token

        if not current.type is closure.begin:
            return False

        self._next_token()

        self._closure_stack.append((closure, current))

        return True

    def _end_closure(self, expected_closure: Closure) -> bool:
        current = self._current_token

        if  not current.type is expected_closure.end:
            return False

        self._next_token()

        try:
            opened_closure = self._closure_stack.pop()

            if opened_closure[0] != expected_closure:
                raise OrphanClosureBeginError(opened_closure[0], opened_closure[1].line, opened_closure[1].column)
        except IndexError:
            # It seems that, if this one is ever raised, it'll be most likely an error in the parsing process.
            raise OrphanClosureEndError(expected_closure, current.line, current.column)

        return True

    def _handle_unexpected_token(self) -> None:
        if self._current_token.type is TokenType.END:
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
        ended_closure = next((c for c in Closure if c.end==self._current_token.type), None)

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
