from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock
import os
import sys

class UVSimCore:
    # IO
    READ = 10 
    WRITE = 11
    LOAD = 20
    STORE = 21
    # ARITHMETIC
    ADD = 30
    SUBTRACT = 31
    DIVIDE = 32
    MULTIPLY = 33
    # CONTROL
    BRANCH = 40
    BRANCHNEG = 41
    BRANCHZERO = 42
    HALT = 43

    MEMORY_SIZE = 100

    def __init__(self, get_input_callback):
        self.get_input = get_input_callback  # gets user input from console
        self.memory_size = 250
        self.memory = [0] * self.memory_size
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

    def convert_to_6_digit(self, content_lines):
        converted = []
        for line in content_lines:
            line = line.strip()
            if not line:
                continue
            if not (line.startswith('+') or line.startswith('-')):
                continue
            if len(line) != 5:
                raise ValueError(f"Invalid 4-digit word: {line}")
            sign = line[0]              # '+' or '-'
            opcode = line[1:3]          # two digits opcode
            operand = line[3:]           # two digits operand
            # Add leading zero before opcode and operand to make them 3 digits each
            new_word = f"{sign}0{opcode}0{operand}"
            converted.append(new_word)
        return converted

    def load_program(self, filename):
        self.memory = [0] * self.memory_size
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]

            if len(lines) > self.memory_size:
                raise ValueError(f"Program has more than {self.memory_size} lines.")

            # Detect file format
            if all(len(line) == 5 for line in lines):  # 4-digit format (+1007)
                print("Detected 4-digit file. Converting to 6-digit format...")
                lines = self.convert_to_6_digit(lines)

            elif not all(len(line) == 7 for line in lines):  # 6-digit format (+010007)
                raise ValueError("Mixed or invalid instruction format detected.")

            for i, line in enumerate(lines):
                if not (line.startswith('+') or line.startswith('-')):
                    raise ValueError(f"Invalid format at line {i + 1}: {line}")
                # Convert signed string to int and store in memory
                self.memory[i] = int(line)

        except FileNotFoundError:
            print("Error: File not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
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
        # For 6-digit words: first 3 digits = opcode, last 3 digits = operand
        opcode = abs(instruction) // 1000    # first three digits (e.g. 010)
        operand = abs(instruction) % 1000    # last three digits (e.g. 007)

        if operand < 0 or operand > self.memory_size - 1:
            print(f"Invalid memory access at line {self.program_counter}: {operand}")
            self.halted = True
            return

        if opcode == 10:
            # READ opcode = 010
            self.get_input(f"READ to memory [{operand}]:", lambda value: self._handle_read(operand, value))
            return
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

        self.program_counter += 1  # increment if no branch

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
    coreInstance = UVSimCore(sys.stdin)  # start UVSim with the default standard input
    coreInstance.load_program(filename)
    coreInstance.run_program()

if __name__ == "__main__":
    main()
'''
