
def READ(memory, address):
    try:
        value = int(input(f"READ to memory[{address}]: "))
        memory[address] = value
    except ValueError:
        print("Invalid input. Please enter an integer.")
        READ(memory, address)

def WRITE(memory, address):
    print(f"WRITE from memory[{address}]: {memory[address]}")

def LOAD(memory, address, accumulator):
    return memory[address]

def STORE(memory, address, accumulator):
    memory[address] = accumulator
