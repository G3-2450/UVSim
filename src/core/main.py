from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock
import os
import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from interface.gui import ConsoleWidget

class UVSimCore:
    def __init__(self, get_input_callback):
        self.get_input = get_input_callback #gets user input from console
        self.memory = [0] *250
        self.accumulator = 0
        self.program_counter = 0 
        self.halted = False

    # Returns a list of all of the commands in the file.
    def load_program(self, filename):
        self.memory = [0] * 250
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

        try:
            with open(filename, 'r') as f:
                for i, line in enumerate(f):
                    line = line.strip()
                    if line and (line.startswith('+') or line.startswith('-')):
                        self.memory[i] = int(line)
        except FileNotFoundError:
            print("Error: File not found.")
            return None
        return self.memory 

    def run_program(self):
        Clock.schedule_interval(self._run_step, 0.1)

    def _run_step(self, dt):
        if self.halted or self.program_counter >= len(self.memory):
            return False
        self.step()
        
    def step(self):
        if self.halted or self.program_counter >= len(self.memory):
            print("Program Halted or out of bounds")
            return
        
        instruction = self.memory[self.program_counter]
        opcode = abs(instruction) // 1000 # first two digits
        operand = abs(instruction) % 1000 # last two digits

        self.program_counter # used to increment normally

        if opcode == 10:
            # BasicMLOps.read(memory, operand)
            self.get_input(f"READ to memory [{operand}]:", lambda value: self._handle_read(operand, value))
            return 
        elif opcode == 11:
            BasicMLOps.write(self.memory, operand)
        elif opcode == 20:
            accumulator = BasicMLOps.load(self.memory, operand, self.accumulator)
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
                return
        elif opcode == 33:
            self.accumulator = BasicMLOps.multiply(self.accumulator, self.memory[operand])
        elif opcode == 40:
            self.program_counter = BasicMLOps.branch(operand)
            return
        elif opcode == 41:
            self.program_counter = BasicMLOps.branch_neg(self.program_counter, operand, self.accumulator)
            return
        elif opcode == 42:
            self.program_counter = BasicMLOps.branch_zero(self.program_counter, operand, self.accumulator)
            return
        elif opcode == 43:
            BasicMLOps.halt()
            self.halted = True
            return
        else:
            print(f"Unknown instruction: {instruction}")
            self.halted = True
            return

        self.program_counter += 1 # only increment if not branched

    def _handle_read(self, address, value):
        try:
            self.memory[address] = int(value)
            self.program_counter += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
'''
# test input handler (console-based testing)
def main():
    filename = input("Enter the BasicML program file (e.g. test1.txt): ").strip()

    # not currently working
    coreInstance = UVSimCore(sys.stdin) # start UVSim with the default standard input

    coreInstance.load_program(filename)
    coreInstance.run_program()

if __name__ == "__main__":
    main()
'''
