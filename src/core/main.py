from BasicMLOps import BasicMLOps

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
            BasicMLOps.read(memory, operand)
        elif opcode == 11:
            BasicMLOps.write(memory, operand)
        elif opcode == 20:
            accumulator = BasicMLOps.load(memory, operand, accumulator)
        elif opcode == 21:
            BasicMLOps.store(memory, operand, accumulator)
        elif opcode == 30:
            accumulator = BasicMLOps.add(accumulator, memory[operand])
        elif opcode == 31:
            accumulator = BasicMLOps.subtract(accumulator, memory[operand])
        elif opcode == 32:
            try:
                accumulator = BasicMLOps.divide(accumulator, memory[operand])
            except ZeroDivisionError as e:
                print(e)
                break
        elif opcode == 33:
            accumulator = BasicMLOps.multiply(accumulator, memory[operand])
        elif opcode == 40:
            program_counter = BasicMLOps.branch(operand)
            continue
        elif opcode == 41:
            program_counter = BasicMLOps.branch_neg(program_counter, operand, accumulator)
            continue
        elif opcode == 42:
            program_counter = BasicMLOps.branch_zero(program_counter, operand, accumulator)
            continue
        elif opcode == 43:
            BasicMLOps.halt()
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
