'''
Executes program instructions and operands
InstructionExecutor.py
'''
from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock

class InstructionExecutor:
    # Opcodes
    READ = 10
    WRITE = 11
    LOAD = 20
    STORE = 21
    ADD = 30
    SUBTRACT = 31
    DIVIDE = 32
    MULTIPLY = 33
    BRANCH = 40
    BRANCHNEG = 41
    BRANCHZERO = 42
    HALT = 43
    
    def __init__(self, memory_model, get_input_callback):
        self.memory_model = memory_model
        self.get_input = get_input_callback
    # Dispatch table
        self.opcode_handlers = {
            self.READ: self._handle_read_op,
            self.WRITE: self._handle_write_op,
            self.LOAD: self._handle_load_op,
            self.STORE: self._handle_store_op,
            self.ADD: self._handle_add_op,
            self.SUBTRACT: self._handle_subtract_op,
            self.DIVIDE: self._handle_divide_op,
            self.MULTIPLY: self._handle_multiply_op,
            self.BRANCH: self._handle_branch_op,
            self.BRANCHNEG: self._handle_branch_neg_op,
            self.BRANCHZERO: self._handle_branch_zero_op,
            self.HALT: self._handle_halt_op
        }
        
    def run_program(self):
        Clock.schedule_interval(self._run_step, 0.1)

    def _run_step(self, dt):
        if self.memory_model.halted or self.memory_model.program_counter >= len(self.memory_model.memory):
            return False
        self.step()

    def step(self):
        if self.halted or self.program_counter >= len(self.memory):
            print("Program Halted or out of bounds")
            return

        instruction = self.memory[self.program_counter]
        opcode = abs(instruction) // 1000
        operand = abs(instruction) % 1000

        if operand < 0 or operand >= self.memory_size:
            print(f"Invalid memory access at line {self.program_counter}: {operand}")
            self.halted = True
            return

        handler = self.opcode_handlers.get(opcode, self._handle_invalid_op)

        if opcode == self.READ:
            # Handle READ async input
            handler(operand)
            return

        handler(operand)
        if opcode not in {self.BRANCH, self.BRANCHNEG, self.BRANCHZERO, self.HALT}:
            self.program_counter += 1

    # Handlers
    def _handle_read_op(self, operand):
        self.get_input(f"READ to memory [{operand}]:", lambda value: self._handle_read_value(operand, value))

    def _handle_read_value(self, address, value):
        try:
            self.memory[address] = int(value)
            self.program_counter += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")

    def _handle_write_op(self, operand):
        BasicMLOps.write(self.memory, operand)

    def _handle_load_op(self, operand):
        self.accumulator = BasicMLOps.load(self.memory, operand, self.accumulator)

    def _handle_store_op(self, operand):
        BasicMLOps.store(self.memory, operand, self.accumulator)

    def _handle_add_op(self, operand):
        self.accumulator = BasicMLOps.add(self.accumulator, self.memory[operand])

    def _handle_subtract_op(self, operand):
        self.accumulator = BasicMLOps.subtract(self.accumulator, self.memory[operand])

    def _handle_divide_op(self, operand):
        try:
            self.accumulator = BasicMLOps.divide(self.accumulator, self.memory[operand])
        except ZeroDivisionError as e:
            print(e)
            self.halted = True

    def _handle_multiply_op(self, operand):
        self.accumulator = BasicMLOps.multiply(self.accumulator, self.memory[operand])

    def _handle_branch_op(self, operand):
        self.program_counter = BasicMLOps.branch(operand)

    def _handle_branch_neg_op(self, operand):
        self.program_counter = BasicMLOps.branch_neg(self.program_counter, operand, self.accumulator)

    def _handle_branch_zero_op(self, operand):
        self.program_counter = BasicMLOps.branch_zero(self.program_counter, operand, self.accumulator)

    def _handle_halt_op(self, operand):
        BasicMLOps.halt()
        self.halted = True

    def _handle_invalid_op(self, operand):
        print(f"Unknown instruction at PC {self.program_counter}")
        self.halted = True

