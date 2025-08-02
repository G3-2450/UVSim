'''
Executes program instructions and operands
InstructionExecutor.py
'''
from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock

class InstructionExecutor:
    def __init__(self, memory_model, get_input_callback):
        self.memory_model = memory_model
        self.get_input = get_input_callback

    def run_program(self):
        Clock.schedule_interval(self._run_step, 0.1)

    def _run_step(self, dt):
        if self.memory_model.halted or self.memory_model.program_counter >= len(self.memory_model.memory):
            return False
        self.step()

    def step(self):
        if self.memory_model.halted or self.memory_model.program_counter >= len(self.memory_model.memory):
            print("Program Halted or out of bounds")
            return

        instruction = self.memory_model.memory[self.memory_model.program_counter]
        # For 6-digit words: first 3 digits = opcode, last 3 digits = operand
        opcode = abs(instruction) // 1000    # first three digits (e.g. 010)
        operand = abs(instruction) % 1000    # last three digits (e.g. 007)

        if operand < 0 or operand > 249:
            print(f"Invalid memory access at line {self.memory_model.program_counter}: {operand}")
            self.memory_model.halted = True
            return

        if opcode == 10:
            # READ opcode = 010
            self.get_input(f"READ to memory [{operand}]:", lambda value: self._handle_read(operand, value))
            return
        elif opcode == 11:
            BasicMLOps.write(self.memory_model.memory, operand)
        elif opcode == 20:
            self.memory_model.accumulator = BasicMLOps.load(self.memory_model.memory, operand)
        elif opcode == 21:
            BasicMLOps.store(self.memory_model.memory, operand, self.memory_model.accumulator)
        elif opcode == 30:
            self.memory_model.accumulator = BasicMLOps.add(self.accumulator, self.memory[operand])
        elif opcode == 31:
            self.accumulator = BasicMLOps.subtract(self.memory_model.accumulator, self.memory_model.memory[operand])
        elif opcode == 32:
            try:
                self.memory_model.accumulator = BasicMLOps.divide(self.memory_model.accumulator, self.memory_model.memory[operand])
            except ZeroDivisionError as e:
                print(e)
                return
        elif opcode == 33:
            self.memory_model.accumulator = BasicMLOps.multiply(self.memory_model.accumulator, self.memory_model.memory[operand])
        elif opcode == 40:
            self.memory_model.program_counter = BasicMLOps.branch(operand)
            return
        elif opcode == 41:
            self.memory_model.program_counter = BasicMLOps.branch_neg(self.memory_model.program_counter, operand, self.memory_model.accumulator)
            return
        elif opcode == 42:
            self.program_counter = BasicMLOps.branch_zero(self.memory_model.program_counter, operand, self.memory_model.accumulator)
            return
        elif opcode == 43:
            BasicMLOps.halt()
            self.memory_model.halted = True
            return
        else:
            print(f"Unknown instruction: {instruction}")
            self.memory_model.halted = True
            return

        self.memory_model.program_counter += 1  # increment if no branch

    def _handle_read(self, address, value):
        try:
            self.memory_model.memory[address] = int(value)
            self.memory_model.program_counter += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")
