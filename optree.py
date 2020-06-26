from random import randint


class Operation:
    """Base-class of the executable operations to which Py-Dician expressions are translated.

    An operation takes zero or more operands, which act as its parameters. Each operand should
    also be an operation that results in a value of a type accepted by the main operation.
    """

    def run(self):
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
    def __init__(self, value):
        super().__init__()
        self._value = value

    def run(self):
        return self._value


class DieOp(UnaryOp):
    def run(self):
        return lambda: randint(1, self._operand.run())


class DiceRollOp(BinaryOp):
    def __init__(self, left_operand: Operation, right_operand: Operation):
        super().__init__(left_operand, DieOp(right_operand))

    def run(self):
        dice_count = self._left_operand.run()
        die = self._right_operand.run()

        return sum(die() for i in range(dice_count))


class NegateOp(UnaryOp):
    def run(self):
        return -self._operand.run()


class SumOp(BinaryOp):
    def run(self):
        return self._left_operand.run() + self._right_operand.run()


class SubtractOp(BinaryOp):
    def run(self):
        return self._left_operand.run() - self._right_operand.run()


class MultiplyOp(BinaryOp):
    def run(self):
        return self._left_operand.run() * self._right_operand.run()


class DivideOp(BinaryOp):
    def run(self):
        return self._left_operand.run() / self._right_operand.run()


if __name__ == "__main__":
    # Equivalent to "10 * (1d10 - 1) + 1d10".
    dice_roll = SumOp(
        MultiplyOp(
            LiteralValueOp(10),
            SubtractOp(
                DiceRollOp(
                    LiteralValueOp(1),
                    LiteralValueOp(10)
                ),
                LiteralValueOp(1)
            )
        ),
        DiceRollOp(
            LiteralValueOp(1),
            LiteralValueOp(10)
        )
    )
    print(dice_roll.run())
