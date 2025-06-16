'''
CS 2450 - Final Group Project - UVUSim
Milestone 2: Unit Testing 
Unit Tests - Arithmetic Operations (ADD, SUBTRACT, DIVIDE, and MULTIPLY)
'''

#Arithmetic operation:
#ADD = 30 Add a word from a specific location in memory to the 
#    word in the accumulator (leave the result in the accumulator)
#SUBTRACT = 31 Subtract a word from a specific location in 
#    memory from the word in the accumulator (leave the result in the accumulator)
#DIVIDE = 32 Divide the word in the accumulator by a word from 
#    a specific location in memory (leave the result in the accumulator).
#MULTIPLY = 33 multiply a word from a specific location in 
#    memory to the word in the accumulator (leave the result in the accumulator).

import unittest
from arithmetic_ops import ADD, SUBTRACT, DIVIDE, MULTIPLY 

class TestArithmeticOps(unittest.TestCase):
    #ADD Tests
    def test_add_positive_nums(self):
        self.assertEqual(ADD(10, 5), 15)

    def test_add_negative_nums(self):
        self.assertEqual(ADD(10, -3), 7)

    #SUBTRACT Tests
    def test_subtract_positive_nums(self):
        self.assertEqual(SUBTRACT(10, 5), 5)

    def test_subtract_negative_nums(self):
        self.assertEqual(SUBTRACT(5, 10), -5)

    #DIVIDE Tests
    def test_divide_positive_nums(self):
        self.assertEqual(DIVIDE(10, 5), 2)

    def test_divide_by_zero_nums(self):
        with self.assertRaises(ZeroDivisionError):
            DIVIDE(10, 0)

    #MULTIPLY Tests
    def test_mulitply_positive_nums(self):
        self.assertEqual(MULTIPLY(10, 5), 50)

    def test_mulitply_by_zero_nums(self):
        self.assertEqual(MULTIPLY(10, 0), 0)

if __name__ == '__main__':
    unittest.main()