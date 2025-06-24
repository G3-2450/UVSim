from BasicMLOps import BasicMLOps
import unittest

class TestControlOps(unittest.TestCase):
    #BRANCH
    def test_branch(self):
        self.assertEqual(BasicMLOps.branch(5), 5)

    def test_branch_error(self):
        with self.assertRaisesRegex(Exception, r"the nextProgramCounter is less than 0\. nextProgramCounter = -5"):
            BasicMLOps.branch(-5)

    #BRANCHNEG
    def test_branchneg_positive(self):
        self.assertEqual(BasicMLOps.branch_neg(1, 12, 0), 2)

    def test_branchneg_negative(self):
        self.assertEqual(BasicMLOps.branch_neg(2, 15, -5), 15)

    def test_branchneg_error(self):
        with self.assertRaises(Exception):
            BasicMLOps.branch_neg(2, -1, -5)

    #BRANCHZERO
    def test_branchzero_zero(self):
        self.assertEqual(BasicMLOps.branch_zero(1, 12, 0), 12)

    def test_branchzero_positive(self):
        self.assertEqual(BasicMLOps.branch_zero(2, 15, 5), 3)

    def test_branchzero_error(self):
        with self.assertRaisesRegex(Exception, r"the nextProgramCounter is less than 0\. nextProgramCounter = -1"):
            BasicMLOps.branch_zero(2, -1, 0)

    #HALT
    def test_halt(self):
        self.assertIsNone(BasicMLOps.halt())

if __name__ == '__main__':
    unittest.main()