# Control operation:
# BRANCH = 40 Branch to a specific location in memory
# BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
# BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
# HALT = 43 Pause the program


def BRANCH(nextProgramCounter):
    if (nextProgramCounter < 0):
        raise Exception("the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")
    
    print(f"BRANCH: programCounter = nextProgramCounter: {nextProgramCounter}")
    return nextProgramCounter
    

def BRANCHNEG(currentProgramCounter, nextProgramCounter, accumulator):
    if accumulator > 0:
        print(f"BRANCHNEG: programCounter = currentProgramCounter + 1: {currentProgramCounter + 1}")
        return currentProgramCounter + 1
    
    if (nextProgramCounter < 0):
        raise Exception("the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")

    print(f"BRANCHNEG: programCounter = nextProgramCounter: {nextProgramCounter}")
    return nextProgramCounter
        

def BRANCHZERO(currentProgramCounter, nextProgramCounter, accumulator):
    if accumulator != 0:
        print(f"BRANCHZERO: programCounter = currentProgramCounter + 1: {currentProgramCounter + 1}")
        return currentProgramCounter + 1
   
    if (nextProgramCounter < 0):
        raise Exception("the nextProgramCounter is less than 0. nextProgramCounter = {nextProgramCounter}")

    print(f"BRANCHZERO: programCounter = nextProgramCounter: {nextProgramCounter}")
    return nextProgramCounter
        

def HALT():
    print(f"PROGRAM HALTED")
    return None