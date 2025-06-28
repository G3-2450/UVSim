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
    def __init__(self, parameter1, parameter2):
        self.instance_variable1 = parameter1
        self.instance_variable2 = parameter2

    # IO OPERATIONS

    @staticmethod
    def read(memory, address):
        while True:
            try:
                value = int(input(f"READ to memory [{address}]: "))
                memory[address] = value
                break
            except ValueError:
                print ("Invalid input. Please enter an integer.")

    @staticmethod
    def write(memory, address):
        print(f"WRITE from memory[{address}]: {memory[address]}")

    @staticmethod
    def load(memory, address, accumulator):
        print(f"LOAD from memory[{address}]: {memory[address]}")
        return memory[address]

    @staticmethod
    def store(memory, address, accumulator):
        print(f"STORE from accumulator to memory[{address}]: {accumulator}")
        memory[address] = accumulator


    # ARITHMETIC OPERATIONS

    @staticmethod
    def add(accumulator, memory_value):
        print(f"ADD: {accumulator} + {memory_value}")
        return accumulator + memory_value

    @staticmethod
    def subtract(accumulator, memory_value):
        print(f"SUBTRACT: {accumulator} - {memory_value}")
        return accumulator - memory_value

    @staticmethod
    def divide(accumulator, memory_value):
        if memory_value == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        print(f"DIVIDE: {accumulator} // {memory_value}")
        return accumulator // memory_value

    @staticmethod
    def multiply(accumulator, memory_value):
        print(f"MULTIPLY: {accumulator} * {memory_value}")
        return accumulator * memory_value


    # CONTROL OPERATIONS

    @staticmethod
    def branch(nextProgramCounter):
        if (nextProgramCounter < 0):
            raise Exception(f"the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")
        
        print(f"BRANCH: programCounter = nextProgramCounter: {nextProgramCounter}")
        return nextProgramCounter
        
    @staticmethod
    def branch_neg(currentProgramCounter, nextProgramCounter, accumulator):
        if accumulator >= 0:
            print(f"BRANCHNEG: programCounter = currentProgramCounter + 1: {currentProgramCounter + 1}")
            return currentProgramCounter + 1
        
        if (nextProgramCounter < 0):
            raise Exception(f"the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")

        print(f"BRANCHNEG: programCounter = nextProgramCounter: {nextProgramCounter}")
        return nextProgramCounter
            
    @staticmethod
    def branch_zero(currentProgramCounter, nextProgramCounter, accumulator):
        if accumulator != 0:
            print(f"BRANCHZERO: programCounter = currentProgramCounter + 1: {currentProgramCounter + 1}")
            return currentProgramCounter + 1
    
        if (nextProgramCounter < 0):
            raise Exception(f"the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")

        print(f"BRANCHZERO: programCounter = nextProgramCounter: {nextProgramCounter}")
        return nextProgramCounter
            
    @staticmethod
    def halt():
        print(f"PROGRAM HALTED")
        return None
    
