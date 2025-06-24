class BasicMLOps:
    def __init__(self, parameter1, parameter2):
        self.instance_variable1 = parameter1
        self.instance_variable2 = parameter2

    # IO OPERATIONS

    @staticmethod
    def read(memory, address):
        try:
            value = int(input(f"READ to memory[{address}]: "))
            memory[address] = value
        except ValueError:
            print("Invalid input. Please enter an integer.")
            BasicMLOps.read(memory, address)

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
    