import unittest
import pydician


class TestOperation(unittest.TestCase):
    def test_Operation_cannot_be_run(self):
        with self.assertRaises(NotImplementedError):
            pydician.Operation().run()


class TestLiteralValueOp(unittest.TestCase):
    def test_returns_unmodified(self):
        test_values = [None, True, False, 0, 1, -1,
                       0.5, -0.5, 'Something', 'Something else']
        for tv in test_values:
            self.assertEqual(pydician.LiteralValueOp(tv).run(), tv)


class TestDieOp(unittest.TestCase):
    def test_returns_callable(self):
        self.assertTrue(callable(pydician.DieOp(pydician.LiteralValueOp(6)).run()))

    def test_die_generates_int(self):
        die = pydician.DieOp(pydician.LiteralValueOp(6)).run()
        self.assertEqual(type(die()), int)


class TestDiceRollOp(unittest.TestCase):
    def test_returns_int(self):
        result = pydician.DiceRollOp(pydician.LiteralValueOp(2),
                                     pydician.DieOp(pydician.LiteralValueOp(6))).run()
        self.assertEqual(type(result), int)


class TestSingleDieRollOp(unittest.TestCase):
    def test_returns_int(self):
        result = pydician.SingleDieRollOp(pydician.DieOp(pydician.LiteralValueOp(6))).run()
        self.assertEqual(type(result), int)


class _TestArithmeticOp(unittest.TestCase):
    _TEST_VALUES = [0, 1, -1, 0.5, -0.5, 1.5, -1.5]


class TestNegateOp(_TestArithmeticOp):
    def test_returns_arithmetic_negate(self):
        for tv in super()._TEST_VALUES:
            self.assertEqual(pydician.NegateOp(pydician.LiteralValueOp(tv)).run(), -tv)


class TestSumOp(_TestArithmeticOp):
    def test_returns_sum(self):
        for ltv in super()._TEST_VALUES:
            for rtv in super()._TEST_VALUES:
                self.assertEqual(pydician.SumOp(pydician.LiteralValueOp(ltv),
                                                pydician.LiteralValueOp(rtv)).run(),
                                 ltv+rtv)


class TestSubtractOp(_TestArithmeticOp):
    def test_returns_sum(self):
        for ltv in super()._TEST_VALUES:
            for rtv in super()._TEST_VALUES:
                self.assertEqual(pydician.SubtractOp(pydician.LiteralValueOp(ltv),
                                                     pydician.LiteralValueOp(rtv)).run(),
                                 ltv-rtv)
