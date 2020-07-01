import unittest
import pydician


class TestOperations(unittest.TestCase):
    def test_Operation_cannot_be_run(self):
        with self.assertRaises(NotImplementedError):
            pydician.Operation().run()

    def test_LiteralValueOp_returns_unmodified(self):
        self.assertEqual(pydician.LiteralValueOp(0).run(), 0)
        self.assertEqual(pydician.LiteralValueOp(1).run(), 1)
        self.assertEqual(pydician.LiteralValueOp(-1).run(), -1)
        self.assertEqual(pydician.LiteralValueOp(0.5).run(), 0.5)
        self.assertEqual(pydician.LiteralValueOp(-0.5).run(), -0.5)
        self.assertEqual(pydician.LiteralValueOp('Something').run(), 'Something')
        self.assertEqual(pydician.LiteralValueOp('Something else').run(), 'Something else')
