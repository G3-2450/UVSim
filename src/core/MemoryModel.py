"""
Initializes and manages memory storage, registers, and program state.
"""

class MemoryModel:
    """
    Represents the memory and register state for the BasicML simulator.

    Attributes:
        memory (list of int): List of 250 integer memory slots initialized to 0.
        accumulator (int): The accumulator register for arithmetic operations.
        program_counter (int): The address of the next instruction to execute.
        halted (bool): Flag indicating whether the program has halted.
    """

    def __init__(self):
        """
        Initializes the memory, accumulator, program counter, and halted flag.
        All 250 memory slots start at 0, and registers are reset.
        """
        self.memory = [0] * 250
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def reset(self):
        """
        Resets memory and registers to their initial state.

        Clears all memory slots to 0, resets accumulator and program counter,
        and clears the halted flag to allow a fresh program run.
        """
        self.memory = [0] * 250
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False
