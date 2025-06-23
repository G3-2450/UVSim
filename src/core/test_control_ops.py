from control_ops import BRANCH, BRANCHNEG, BRANCHZERO, HALT
import unittest

class TestControlOps(unittest.TestCase):
    #BRANCH
    def test_branch(self):
        self.assertEqual(BRANCH(5), 5)

    def test_branch_error(self):
        with self.assertRaisesRegex(Exception, r"the nextProgramCounter is less than 0\. nextProgramCounter = -5"):
            BRANCH(-5)

    #BRANCHNEG
    def test_branchneg_positive(self):
        self.assertEqual(BRANCHNEG(1, 12, 0), 2)

    def test_branchneg_negative(self):
        self.assertEqual(BRANCHNEG(2, 15, -5), 15)

    def test_branchneg_error(self):
        with self.assertRaises(Exception):
            BRANCHNEG(2, -1, -5)

    #BRANCHZERO
    def test_branchzero_zero(self):
        self.assertEqual(BRANCHZERO(1, 12, 0), 12)

    def test_branchzero_positive(self):
        self.assertEqual(BRANCHZERO(2, 15, 5), 3)

    def test_branchzero_error(self):
        with self.assertRaisesRegex(Exception, r"the nextProgramCounter is less than 0\. nextProgramCounter = -1"):
            BRANCHZERO(2, -1, 0)

    #HALT
    def test_halt(self):
        self.assertIsNone(HALT())

if __name__ == '__main__':
    unittest.main()