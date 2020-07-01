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
        self.assertTrue(callable(pydician.DieOp(pydician.LiteralValueOp(6)).run()))

    def test_die_generates_int(self):
        die = pydician.DieOp(pydician.LiteralValueOp(6)).run()
        self.assertEqual(type(die()), int)


class TestDiceRollOp(unittest.TestCase):
    def test_returns_int(self):
        result = pydician.DiceRollOp(pydician.LiteralValueOp(2), pydician.DieOp(pydician.LiteralValueOp(6))).run()
        self.assertEqual(type(result), int)


class TestSingleDieRollOp(unittest.TestCase):
    def test_returns_int(self):
        result = pydician.SingleDieRollOp(pydician.DieOp(pydician.LiteralValueOp(6))).run()
        self.assertEqual(type(result), int)


class TestNegateOp(unittest.TestCase):
    def test_returns_arithmetic_negate(self):
        test_values = [
                0,
                1,
                -1,
                0.5,
                -0.5,
                1.5,
                -1.5
            ]
        for tv in test_values:
            self.assertEqual(pydician.NegateOp(pydician.LiteralValueOp(tv)).run(), -tv)
