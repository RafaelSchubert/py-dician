import unittest
import pydician


class TestOperation(unittest.TestCase):
    def test_Operation_cannot_be_run(self):
        with self.assertRaises(NotImplementedError):
            pydician.Operation().run()


class TestLiteralValueOp(unittest.TestCase):
    def test_returns_unmodified(self):
        test_values = [
                None,
                True,
                False,
                0,
                1,
                -1,
                0.5,
                -0.5,
                'Something',
                'Something else'
            ]
        for tv in test_values:
            self.assertEqual(pydician.LiteralValueOp(tv).run(), tv)


class TestDieOp(unittest.TestCase):
    def test_returns_callable(self):
        op = pydician.DieOp(pydician.LiteralValueOp(6))
        self.assertTrue(callable(op.run()))

    def test_die_generates_int(self):
        op = pydician.DieOp(pydician.LiteralValueOp(6))
        die = op.run()
        self.assertEqual(type(die()), int)


class TestDiceRollOp(unittest.TestCase):
    def test_returns_int(self):
        op = pydician.DiceRollOp(pydician.LiteralValueOp(2),
                                 pydician.DieOp(pydician.LiteralValueOp(6)))
        result = op.run()
        self.assertEqual(type(result), int)


class TestSingleDieRollOp(unittest.TestCase):
    def test_returns_int(self):
        op = pydician.SingleDieRollOp(pydician.DieOp(pydician.LiteralValueOp(6)))
        result = op.run()
        self.assertEqual(type(result), int)


class _TestArithmeticOp(unittest.TestCase):
    _TEST_VALUES = [
            0,
            1,
            -1,
            0.5,
            -0.5,
            1.5,
            -1.5
        ]


class TestNegateOp(_TestArithmeticOp):
    def test_returns_arithmetic_negate(self):
        for tv in super()._TEST_VALUES:
            op = pydician.NegateOp(pydician.LiteralValueOp(tv))
            self.assertEqual(op.run(), -tv)


class TestSumOp(_TestArithmeticOp):
    def test_returns_sum(self):
        for ltv in super()._TEST_VALUES:
            for rtv in super()._TEST_VALUES:
                op = pydician.SumOp(pydician.LiteralValueOp(ltv),
                                    pydician.LiteralValueOp(rtv))
                self.assertEqual(op.run(), ltv+rtv)


class TestSubtractOp(_TestArithmeticOp):
    def test_returns_subtraction(self):
        for ltv in super()._TEST_VALUES:
            for rtv in super()._TEST_VALUES:
                op = pydician.SubtractOp(pydician.LiteralValueOp(ltv),
                                         pydician.LiteralValueOp(rtv))
                self.assertEqual(op.run(), ltv-rtv)


class TestMultiplyOp(_TestArithmeticOp):
    def test_returns_multiplication(self):
        for ltv in super()._TEST_VALUES:
            for rtv in super()._TEST_VALUES:
                op = pydician.MultiplyOp(pydician.LiteralValueOp(ltv),
                                         pydician.LiteralValueOp(rtv))
                self.assertEqual(op.run(), ltv*rtv)


class TestDivideOp(_TestArithmeticOp):
    def test_returns_division(self):
        for ltv in super()._TEST_VALUES:
            for rtv in super()._TEST_VALUES:
                op = pydician.DivideOp(pydician.LiteralValueOp(ltv),
                                       pydician.LiteralValueOp(rtv))
                if rtv == 0:
                    with self.assertRaises(ZeroDivisionError):
                        op.run()
                else:
                    self.assertEqual(op.run(), ltv/rtv)


class _TestBinaryLogicalComparisonOp(unittest.TestCase):
    _TEST_VALUES = [-2, -1, 0, 1, 2]


class TestSmallerOp(_TestBinaryLogicalComparisonOp):
    def test_returns_less_than(self):
        for lv in super()._TEST_VALUES:
            for rv in super()._TEST_VALUES:
                op = pydician.SmallerOp(pydician.LiteralValueOp(lv),
                                        pydician.LiteralValueOp(rv))
                self.assertEqual(op.run(), 1 if lv<rv else 0)


class TestGreaterOp(_TestBinaryLogicalComparisonOp):
    def test_returns_greater_than(self):
        for lv in super()._TEST_VALUES:
            for rv in super()._TEST_VALUES:
                op = pydician.GreaterOp(pydician.LiteralValueOp(lv),
                                        pydician.LiteralValueOp(rv))
                self.assertEqual(op.run(), 1 if lv>rv else 0)


class TestEqualOp(_TestBinaryLogicalComparisonOp):
    def test_returns_equals_to(self):
        for lv in super()._TEST_VALUES:
            for rv in super()._TEST_VALUES:
                op = pydician.EqualOp(pydician.LiteralValueOp(lv),
                                      pydician.LiteralValueOp(rv))
                self.assertEqual(op.run(), 1 if lv==rv else 0)


class TestSmallerOrEqualOp(_TestBinaryLogicalComparisonOp):
    def test_returns_less_than_or_equals_to(self):
        for lv in super()._TEST_VALUES:
            for rv in super()._TEST_VALUES:
                op = pydician.SmallerOrEqualOp(pydician.LiteralValueOp(lv),
                                               pydician.LiteralValueOp(rv))
                self.assertEqual(op.run(), 1 if lv<=rv else 0)


class TestGreaterOrEqualOp(_TestBinaryLogicalComparisonOp):
    def test_returns_greater_than_or_equals_to(self):
        for lv in super()._TEST_VALUES:
            for rv in super()._TEST_VALUES:
                op = pydician.GreaterOrEqualOp(pydician.LiteralValueOp(lv),
                                               pydician.LiteralValueOp(rv))
                self.assertEqual(op.run(), 1 if lv>=rv else 0)


class TestNotEqualOp(_TestBinaryLogicalComparisonOp):
    def test_returns_not_equals_to(self):
        for lv in super()._TEST_VALUES:
            for rv in super()._TEST_VALUES:
                op = pydician.NotEqualOp(pydician.LiteralValueOp(lv),
                                         pydician.LiteralValueOp(rv))
                self.assertEqual(op.run(), 1 if lv!=rv else 0)
