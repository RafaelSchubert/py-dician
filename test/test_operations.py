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

    def test_die_returns_int(self):
        die = pydician.DieOp(pydician.LiteralValueOp(6)).run()
        self.assertEqual(type(die()), int)
