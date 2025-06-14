# Control operation:
# BRANCH = 40 Branch to a specific location in memory
# BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
# BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
# HALT = 43 Pause the program

def BRANCH(currentProgramCounter, nextProgramCounter):
    currentProgramCounter = nextProgramCounter
    return currentProgramCounter

def BRANCHNEG(currentProgramCounter, nextProgramCounter, accumulator):
    if (accumulator < 0):
        currentProgramCounter = nextProgramCounter
    return currentProgramCounter

def BRANCHZERO(currentProgramCounter, nextProgramCounter, accumulator):
    if (accumulator == 0):
        currentProgramCounter = nextProgramCounter
    return currentProgramCounter

def HALT():
    print(f"PROGRAM HALTED")
    return None

