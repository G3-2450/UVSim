from MemoryModel import MemoryModel
import unittest

class TestMemoryModel(unittest.TestCase):
    #RESET
    def test_reset_positive(self):
        memModel = MemoryModel()      # init
        memModel.memory = [5] * 250   # set mem
        memModel.accumulator = 15     # set accumulator
        memModel.program_counter = 21 # set program counter
        memModel.halted = True        # set halted

        memModel.reset()              # reset values

        # check that values are reset

        self.assertEqual(memModel.memory, [0] * 250 )
        self.assertEqual(memModel.accumulator, 0 )
        self.assertEqual(memModel.program_counter, 0 )
        self.assertEqual(memModel.halted, False )

    
if __name__ == '__main__':
    unittest.main()