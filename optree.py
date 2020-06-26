from typing import Any, Callable, Tuple
from random import randint
from error import PyDicianError


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

        die_maximum = self._operand.run()

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

        dice_count = self._left_operand.run()
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


if __name__ == "__main__":
    # Equivalent to "10 * (1d10 - 1) + 1d10".
    dice_roll = SumOp(
        MultiplyOp(
            LiteralValueOp(10),
            SubtractOp(
                DiceRollOp(
                    LiteralValueOp(1),
                    DieOp(LiteralValueOp(10))
                ),
                LiteralValueOp(1)
            )
        ),
        DiceRollOp(
            LiteralValueOp(1),
            DieOp(LiteralValueOp(10))
        )
    )
    print(dice_roll.run())
