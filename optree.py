from random import randint


class Operation:
    """Base-class for the runnable operations which the Py-Dician expressions are translated to."""

    def run(self):
        """Executes this operation.

        Must be overridden.

        Returns:
            The result of the operation.
        """

        return NotImplementedError


class SimpleOp(Operation):
    """Base-class for operations that take no operands, such as literals."""

    pass


class UnaryOp(Operation):
    """Base-class for operations that take a single operand.

    Parameters:
        operand (Operation): the single operand of this operation.
    """

    def __init__(self, operand: Operation):
        super().__init__()
        self._operand = operand


class BinaryOp(Operation):
    """Base-class for operations that take exactly two operands, a left and a right one.

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
    dice_roll = DiceRollOp(SumOp(LiteralValueOp(1), LiteralValueOp(2)), MultiplyOp(LiteralValueOp(2), LiteralValueOp(3)))
    print(dice_roll.run())
