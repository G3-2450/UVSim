from control_ops import BRANCH, BRANCHNEG, BRANCHZERO, HALT
import unittest

class TestArithmeticOps(unittest.TestCase):
    #BRANCH
    def test_add_positive_nums(self):
        self.assertEqual(BRANCH(5), 5)

    def test_divide_by_zero_nums(self):
        with self.assertRaises(Exception):
            BRANCH(-5)

    #BRANCHNEG
    def test_subtract_positive_nums(self):
        self.assertEqual(BRANCHNEG(1, 12, 0), 2)

    def test_subtract_negative_nums(self):
        self.assertEqual(BRANCHNEG(2, 15, -5), 15)

    def test_subtract_negative_nums(self):
        with self.assertRaises(Exception):
            BRANCHNEG(2, -1, -5)

    #BRANCHZERO
    def test_divide_positive_nums(self):
        self.assertEqual(BRANCHZERO(1, 12, 0), 12)

    def test_divide_positive_nums(self):
        self.assertEqual(BRANCHZERO(2, 15, 5), 3)

    def test_divide_by_zero_nums(self):
        with self.assertRaises(Exception):
            BRANCHZERO(2, -1, 0)

    #HAL
    def test_mulitply_positive_nums(self):
        self.assertIsNone(HALT())

    def test_divide_by_zero_nums(self):
        with self.assertRaises(Exception):
            HALT(5)

if __name__ == '__main__':
    unittest.main()