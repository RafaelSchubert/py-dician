from random import randint


class Operation:
    def run(self):
        return NotImplementedError


class ParamlessOp(Operation):
    pass


class UnaryOp(Operation):
    def __init__(self, operand: Operation):
        super().__init__()
        self._operand = operand


class BinaryOp(Operation):
    def __init__(self, left_operand: Operation, right_operand: Operation):
        super().__init__()
        self._left_operand = left_operand
        self._right_operand = right_operand


class LiteralValueOp(ParamlessOp):
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
