from ProgramLoader import ProgramLoader
from MemoryModel import MemoryModel
import unittest
import os

class TestProgramLoader(unittest.TestCase):
    def setUp(self):
        self.memory_model = MemoryModel()
        self.loader = ProgramLoader(self.memory_model)
        self.current_directory = os.getcwd()

        self.four_bit_file = os.path.join(self.current_directory, "test_4bit.txt")
        self.four_bit_converted_file = os.path.join(self.current_directory, "test_4bit_converted.txt")
        self.six_bit_file = os.path.join(self.current_directory, "test_6bit.txt")
        self.four_bit_extra_nine_file = os.path.join(self.current_directory, "test_4bit_extra9.txt")
        self.six_bit_extra_nine_file = os.path.join(self.current_directory, "test_6bit_extra9.txt")

        self.initial_4bit_memory_model = [
            10007,
            10008,
            20007,
            20008,
            21009,
            11009,
            43000,
            000000,
            000000,
            000000,
            -99099,
        ]
        self.initial_6bit_memory_model = [
            10007,
            10008,
            20007,
            20008,
            21009,
            11009,
            43000,
            000000,
            000000,
            000000,
            -999999,
        ]
        self.four_bit_converted_memory_model = self.initial_4bit_memory_model + [0] * (250 - len(self.initial_4bit_memory_model))
        self.six_bit_converted_memory_model = self.initial_6bit_memory_model + [0] * (250 - len(self.initial_6bit_memory_model))

    def _open_file(self, filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    #CONVERT TO 6 DIGIT
    def test_convert4to6_positive(self):
        four_bit_converted = self.loader.convert_to_6_digit(self._open_file(self.four_bit_file))
        four_bit_converted_known = self._open_file(self.four_bit_converted_file)
        self.assertEqual(four_bit_converted, four_bit_converted_known)

    def test_convert4to6_negative(self):
        with self.assertRaisesRegex(Exception, r"Invalid 4-digit word: \+01109"):
            self.loader.convert_to_6_digit(self._open_file(self.four_bit_extra_nine_file))


    #LOAD PROGRAM
    def test_load_6_positive(self):
        self.loader.load_program(self.six_bit_file)
        self.assertEqual(self.loader.memory_model.memory, self.six_bit_converted_memory_model)

    def test_load_6_negative(self):
        with self.assertRaisesRegex(ValueError, r"Mixed or invalid instruction format detected."):
            self.loader.load_program(self.six_bit_extra_nine_file)

    def test_load_4_positive(self):
        self.loader.load_program(self.four_bit_file)
        self.assertEqual(self.loader.memory_model.memory, self.four_bit_converted_memory_model)

    def test_load_4_negative(self):
        with self.assertRaisesRegex(ValueError, r"Mixed or invalid instruction format detected."):
            self.loader.load_program(self.four_bit_extra_nine_file)

if __name__ == '__main__':
    unittest.main()