# I/O operation:
# READ = 10 Read a word from the keyboard into a specific location in memory.
# WRITE = 11 Write a word from a specific location in memory to screen.

# Load/store operations:
# LOAD = 20 Load a word from a specific location in memory into the accumulator.
# STORE = 21 Store a word from the accumulator into a specific location in memory.

# Arithmetic operation:
# ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
# SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
# DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
# MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

# Control operation:
# BRANCH = 40 Branch to a specific location in memory
# BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
# BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
# HALT = 43 Pause the program

class BasicMLOps:
    # IO OPERATIONS

    @staticmethod
    def write(memory, address):
        #Output the value at the given memory address.
        print(f"WRITE from memory[{address}]: {memory[address]}")

    @staticmethod
    def load(memory, address, accumulator):
        #Load the value from the specified memory address into the accumulator.
        print(f"LOAD from memory[{address}]: {memory[address]}")
        return memory[address]

    @staticmethod
    def store(memory, address, accumulator):
        #Store the current value of the accumulator into the specified memory address.
        print(f"STORE from accumulator to memory[{address}]: {accumulator}")
        memory[address] = accumulator

    # ARITHMETIC OPERATIONS

    @staticmethod
    def add(accumulator, memory_value):
        #Add the memory value to the accumulator and return the result.
        print(f"ADD: {accumulator} + {memory_value}")
        return accumulator + memory_value

    @staticmethod
    def subtract(accumulator, memory_value):
        #Subtract the memory value from the accumulator and return the result.
        print(f"SUBTRACT: {accumulator} - {memory_value}")
        return accumulator - memory_value

    @staticmethod
    def divide(accumulator, memory_value):
        #Divide the accumulator by the memory value (integer division). Raise error if dividing by zero.
        if memory_value == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        print(f"DIVIDE: {accumulator} // {memory_value}")
        return accumulator // memory_value

    @staticmethod
    def multiply(accumulator, memory_value):
        #Multiply the accumulator by the memory value and return the result.
        print(f"MULTIPLY: {accumulator} * {memory_value}")
        return accumulator * memory_value

    # CONTROL OPERATIONS

    @staticmethod
    def branch(nextProgramCounter):
        #Unconditionally branch to the specified memory address.
        if nextProgramCounter < 0:
            raise Exception(f"the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")
        print(f"BRANCH: programCounter = nextProgramCounter: {nextProgramCounter}")
        return nextProgramCounter

    @staticmethod
    def branch_neg(currentProgramCounter, nextProgramCounter, accumulator):
        #Branch to a new memory location if the accumulator is negative, otherwise go to the next instruction.
        if accumulator >= 0:
            print(f"BRANCHNEG: programCounter = currentProgramCounter + 1: {currentProgramCounter + 1}")
            return currentProgramCounter + 1
        if nextProgramCounter < 0:
            raise Exception(f"the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")
        print(f"BRANCHNEG: programCounter = nextProgramCounter: {nextProgramCounter}")
        return nextProgramCounter

    @staticmethod
    def branch_zero(currentProgramCounter, nextProgramCounter, accumulator):
        #Branch to a new memory location if the accumulator is zero, otherwise go to the next instruction.
        if accumulator != 0:
            print(f"BRANCHZERO: programCounter = currentProgramCounter + 1: {currentProgramCounter + 1}")
            return currentProgramCounter + 1
        if nextProgramCounter < 0:
            raise Exception(f"the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")
        print(f"BRANCHZERO: programCounter = nextProgramCounter: {nextProgramCounter}")
        return nextProgramCounter

    @staticmethod
    def halt():
        #Halt the execution of the program.
        print(f"PROGRAM HALTED")
        return None

    
