from io_operations import *
from arithmetic_ops import *
from control_ops import *

# Returns a list of all of the commands in the file.
def load_program(filename):
    memory = [0] * 100
    try:
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line and (line.startswith('+') or line.startswith('-')):
                    memory[i] = int(line)
    except FileNotFoundError:
        print("Error: File not found.")
        exit()
    return memory 

def run_program(memory):
    accumulator = 0
    program_counter = 0

    while program_counter < len(memory):
        instruction = memory[program_counter]
        opcode = abs(instruction) // 100    # first two digits
        operand = abs(instruction) % 100    # last two digits

        if opcode == 10:
            READ(memory, operand)
        elif opcode == 11:
            WRITE(memory, operand)
        elif opcode == 20:
            accumulator = LOAD(memory, operand, accumulator)
        elif opcode == 21:
            STORE(memory, operand, accumulator)
        elif opcode == 30:
            accumulator = ADD(accumulator, memory[operand])
        elif opcode == 31:
            accumulator = SUBTRACT(accumulator, memory[operand])
        elif opcode == 32:
            try:
                accumulator = DIVIDE(accumulator, memory[operand])
            except ZeroDivisionError as e:
                print(e)
                break
        elif opcode == 33:
            accumulator = MULTIPLY(accumulator, memory[operand])
        elif opcode == 40:
            program_counter = BRANCH(operand)
            continue
        elif opcode == 41:
            program_counter = BRANCHNEG(program_counter, operand, accumulator)
            continue
        elif opcode == 42:
            program_counter = BRANCHZERO(program_counter, operand, accumulator)
            continue
        elif opcode == 43:
            HALT()
            break
        else:
            print(f"Unknown instruction: {instruction}")
            break

        program_counter += 1

def main():
    filename = input("Enter the BasicML program file (e.g. test1.txt): ").strip()
    memory = load_program(filename)
    run_program(memory)

if __name__ == "__main__":
    main()
