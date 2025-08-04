import unittest
import tempfile
import os

from core.MemoryModel import MemoryModel
from core.ProgramLoader import ProgramLoader
from core.InstructionExecutor import InstructionExecutor

class TestUVSim(unittest.TestCase):

    def setUp(self):
        self.memory = MemoryModel()
        self.inputs = iter(["42", "-5"])
        self.executor = InstructionExecutor(self.memory, lambda prompt, cb: cb(int(next(self.inputs))))
        self.loader = ProgramLoader(self.memory)

    def test_memory_initialization(self):
        self.assertEqual(self.memory.memory, [0] * 250)
        self.assertEqual(self.memory.accumulator, 0)
        self.assertEqual(self.memory.program_counter, 0)
        self.assertFalse(self.memory.halted)

    def test_memory_reset(self):
        self.memory.memory[0] = 999
        self.memory.accumulator = 100
        self.memory.program_counter = 10
        self.memory.halted = True
        self.memory.reset()
        self.assertEqual(self.memory.memory, [0] * 250)
        self.assertEqual(self.memory.accumulator, 0)
        self.assertEqual(self.memory.program_counter, 0)
        self.assertFalse(self.memory.halted)

    def test_program_loader_conversion(self):
        lines = ["+1007"]
        converted = self.loader.convert_to_6_digit(lines)
        self.assertEqual(converted, ["+010007"])

    def test_program_loader_invalid_4_digit(self):
        with self.assertRaises(ValueError):
            self.loader.convert_to_6_digit(["+10"])

    def test_program_loader_skips_invalid_lines(self):
        converted = self.loader.convert_to_6_digit(["Hello", "+1007", "   ", "-2302"])
        self.assertEqual(converted, ["+010007", "-023002"])

    def test_program_loader_with_invalid_format(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write("+100\n+200003\n")
            filename = f.name

        result = self.loader.load_program(filename)
        self.assertIsNone(result)
        os.remove(filename)

    def test_program_loader_with_valid_4_digit_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write("+1007\n+2007\n+4300\n")
            filename = f.name

        result = self.loader.load_program(filename)
        self.assertEqual(result[0], 1007)
        os.remove(filename)

    def test_program_execution_basic_io(self):
        self.memory.memory[0] = +10000  # Read input into mem[0]
        self.memory.memory[1] = +20000  # Load mem[0]
        self.memory.memory[2] = +21001  # Store to mem[1]
        self.memory.memory[3] = +43000  # Halt

        for _ in range(4):
            self.executor.step()

        self.assertEqual(self.memory.memory[0], 42)
        self.assertEqual(self.memory.memory[1], 42)
        self.assertEqual(self.memory.accumulator, 42)
        self.assertTrue(self.memory.halted)

    def test_invalid_opcode(self):
        self.memory.memory[0] = +99000  # Invalid opcode
        self.executor.step()
        self.assertTrue(self.memory.halted)

    def test_invalid_memory_access(self):
        self.memory.memory[0] = +20000
        self.memory.memory[1] = +20250  # Out of range

        self.executor.step()
        self.executor.step()
        self.assertTrue(self.memory.halted)

    def test_branching_opcodes(self):
        self.memory.memory[0] = +40004  # BR to 4
        self.memory.memory[1] = +43000  # Should be skipped
        self.memory.memory[4] = +43000  # Halt

        for _ in range(2):
            self.executor.step()

        self.assertEqual(self.memory.program_counter, 5)
        self.assertTrue(self.memory.halted)

    def test_branch_if_zero(self):
        self.memory.accumulator = 0
        self.memory.memory[0] = +41002  # BRZ 2
        self.memory.memory[2] = +43000  # Halt

        for _ in range(2):
            self.executor.step()
        self.assertTrue(self.memory.halted)

    def test_branch_if_negative(self):
        self.memory.accumulator = -10
        self.memory.memory[0] = +42002  # BRN 2
        self.memory.memory[2] = +43000  # Halt

        for _ in range(2):
            self.executor.step()
        self.assertTrue(self.memory.halted)

    def test_arithmetic_operations(self):
        self.memory.memory[10] = 5
        self.memory.memory[11] = 2
        self.memory.memory[0] = +2010  # Load 5
        self.memory.memory[1] = +3011  # Add 2
        self.memory.memory[2] = +2112  # Store to mem[12]
        self.memory.memory[3] = +3111  # Subtract 2
        self.memory.memory[4] = +3210  # Multiply by 5
        self.memory.memory[5] = +3311  # Divide by 2
        self.memory.memory[6] = +43000  # Halt

        while not self.memory.halted:
            self.executor.step()

        self.assertEqual(self.memory.accumulator, 17)  # (((5 + 2) - 2) * 5) / 2 = 17
        self.assertEqual(self.memory.memory[12], 7)

    def test_add_negative(self):
        self.memory.memory[0] = +30001
        self.memory.memory[1] = -10
        self.memory.accumulator = 5
        self.executor.step()
        self.assertEqual(self.memory.accumulator, -5)

    def test_subtract_negative(self):
        self.memory.memory[0] = +31001
        self.memory.memory[1] = -3
        self.memory.accumulator = -2
        self.executor.step()
        self.assertEqual(self.memory.accumulator, 1)

    def test_multiply_negative(self):
        self.memory.memory[0] = +33001
        self.memory.memory[1] = -4
        self.memory.accumulator = 3
        self.executor.step()
        self.assertEqual(self.memory.accumulator, -12)

    def test_divide_negative(self):
        self.memory.memory[0] = +32001
        self.memory.memory[1] = -2
        self.memory.accumulator = 6
        self.executor.step()
        self.assertEqual(self.memory.accumulator, -3)

    def test_divide_zero(self):
        self.memory.memory[0] = +32001
        self.memory.memory[1] = 0
        self.memory.accumulator = 10
        self.executor.step()
        self.assertTrue(self.memory.halted)
    
    def test_branch_not_taken_when_positive(self):
        self.memory.accumulator = 5
        self.memory.memory[0] = +41010  # BranchNeg to 10
        self.executor.step()
        self.assertEqual(self.memory.program_counter, 1)  # Didn’t branch

    def test_branch_zero_not_taken_when_nonzero(self):
        self.memory.accumulator = 99
        self.memory.memory[0] = +42010  # BranchZero to 10
        self.executor.step()
        self.assertEqual(self.memory.program_counter, 1)  # Didn’t branch

    def test_unknown_opcode(self):
        self.memory.memory[0] = +99999
        self.executor.step()
        self.assertTrue(self.memory.halted)
    
    def test_convert_ignores_comments_and_blanks(self):
        lines = ["+1007", "# comment", "", "+2008"]
        result = self.loader.convert_to_6_digit(lines)
        self.assertEqual(result, ["+010007", "+020008"])

    def test_load_program_with_invalid_line(self):
        # Simulate bad file input
        bad_lines = ["hello world", "+3002"]
        with self.assertRaises(ValueError):
            self.loader.convert_to_6_digit(bad_lines)



if __name__ == "__main__":
    unittest.main()
