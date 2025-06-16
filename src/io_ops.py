
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
    print(f"LOAD from memory[{address}]: {memory[address]}")
    return memory[address]

def STORE(memory, address, accumulator):
    print(f"STORE from accumulator to memory[{address}]: {accumulator}")
    memory[address] = accumulator
