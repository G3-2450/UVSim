'''
Initializes memory storage
'''

class MemoryModel:
    # Initial memory, accumulator, and program counter set up (all valules default to 0 including all 250 memory slots) 
    def __init__(self):
        self.memory = [0] * 250
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def reset(self):
        # Resets all values to default
        self.memory = [0] * 250
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False
