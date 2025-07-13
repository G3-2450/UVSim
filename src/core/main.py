from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock
import os
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from interface.gui import ConsoleWidget

# Returns a list of all of the commands in the file.
class UVSimCore:
    def __init__(self, console_input):
        # self.get_input = console_input
        # self.operations = BasicMLOps(console_input, self.run_program)
        self.get_input = console_input
        self.program_counter = 0
        self.accumulator = 0
        self.memory = [0] * 100

    def load_program(self, filename):
        try:
            with open(filename, 'r') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if line and (line.startswith('+') or line.startswith('-')):
                        self.memory[i] = int(line)
        except FileNotFoundError:
            print("Error: File not found.")
            exit()
        return self.memory 
    
    def input_callback(self, operand, user_input):
        self.memory[operand] = int(user_input)
        Clock.schedule_once(self.run_program, 0) # gives kivy the chance to update ui

    def run_program(self, *args):
        memory = self.memory

        if self.program_counter >= len(self.memory):
            print("program has finished running")
            return
        
        instruction = self.memory[self.program_counter]
        opcode = abs(instruction) // 100    # first two digits
        operand = abs(instruction) % 100    # last two digits

        if opcode == 10:
            # self.operations.read(memory, operand)
            self.get_input(
                promptText=f"READ to memory [{operand}]: ",
                InputFunction=lambda user_input: self.input_callback(operand, user_input)
            )
        elif opcode == 11:
            BasicMLOps.write(self.memory, operand)
        elif opcode == 20:
            self.accumulator = BasicMLOps.load(self.memory, operand, self.accumulator)
        elif opcode == 21:
            BasicMLOps.store(self.memory, operand, self.accumulator)
        elif opcode == 30:
            self.accumulator = BasicMLOps.add(self.accumulator, self.memory[operand])
        elif opcode == 31:
            self.accumulator = BasicMLOps.subtract(self.accumulator, self.memory[operand])
        elif opcode == 32:
            try:
                self.accumulator = BasicMLOps.divide(self.accumulator, self.memory[operand])
            except ZeroDivisionError as e:
                print(e)
                # break
        elif opcode == 33:
            self.accumulator = BasicMLOps.multiply(self.accumulator, self.memory[operand])
        elif opcode == 40:
            self.program_counter = BasicMLOps.branch(operand)
            # continue
        elif opcode == 41:
            self.program_counter = BasicMLOps.branch_neg(self.program_counter, operand, self.accumulator)
            # continue
        elif opcode == 42:
            self.program_counter = BasicMLOps.branch_zero(self.program_counter, operand, self.accumulator)
            # continue
        elif opcode == 43:
            BasicMLOps.halt()
            # break
        else:
            print(f"Unknown instruction: {instruction}")
            # break

        self.program_counter += 1


def main():
    filename = input("Enter the BasicML program file (e.g. test1.txt): ").strip()

    # not currently working
    coreInstance = UVSimCore(sys.stdin) # start UVSim with the default standard input

    coreInstance.load_program(filename)
    coreInstance.run_program()

if __name__ == "__main__":
    main()
