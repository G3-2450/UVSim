from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock
import os
import sys

class UVSimCore:
    """
    UVSimCore handles the core functionality of the BasicML simulator, including
    memory, program loading, instruction execution, and control flow.
    """
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

    def __init__(self, get_input_callback):
        """
        Initialize the simulator with default memory and register values.
        Args:
            get_input_callback (function): Callback function for READ instructions
                                            to handle asynchronous user input.
        """
        self.get_input = get_input_callback
        self.memory_size = 250
        self.memory = [0] * self.memory_size
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

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

    def convert_to_6_digit(self, content_lines):
        """
        Convert 4-digit machine instructions to 6-digit format with leading zeros.
        Args:
            content_lines (list): List of string lines containing 4-digit instructions.
        Returns:
            list: List of converted 6-digit instructions.
        """
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
        """
        Load a BasicML program from a file into memory.
        Args:
            filename (str): The path to the .txt file containing machine code.
        Returns:
            list or None: Memory array if successful, or None on error.
        """
        self.memory = [0] * self.memory_size
        self.accumulator = 0
        self.program_counter = 0
        self.halted = False

        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]

            if len(lines) > self.memory_size:
                raise ValueError(f"Program has more than {self.memory_size} lines.")

            if all(len(line) == 5 for line in lines):
                print("Detected 4-digit file. Converting to 6-digit format...")
                lines = self.convert_to_6_digit(lines)
            elif not all(len(line) == 7 for line in lines):
                raise ValueError("Mixed or invalid instruction format detected.")

            for i, line in enumerate(lines):
                if not (line.startswith('+') or line.startswith('-')):
                    raise ValueError(f"Invalid format at line {i + 1}: {line}")
                self.memory[i] = int(line)

        except FileNotFoundError:
            print("Error: File not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None

        return self.memory

    def run_program(self):
    #Start timed execution of the loaded program. Executes in intervals.
        Clock.schedule_interval(self._run_step, 0.1)

    def _run_step(self, dt):
        """
        A timed step callback that runs one instruction per interval.

        Args:
            dt (float): Delta time passed by Kivy Clock.
        """
        if self.halted or self.program_counter >= len(self.memory):
            return False
        self.step()

    def step(self):
    #Execute a single instruction from memory at the current program counter.
    #Handles branching and halting as necessary.

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
        """
        Initiates asynchronous input request for a READ instruction.

        Args:
            operand (int): Memory address to store the input.
        """
        self.get_input(f"READ to memory [{operand}]:", lambda value: self._handle_read_value(operand, value))

    def _handle_read_value(self, address, value):
        """
        Handles the value returned from the user input callback.

        Args:
            address (int): Memory location to store the input.
            value (str): Input string provided by the user.
        """
        try:
            self.memory[address] = int(value)
            self.program_counter += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")

    def _handle_write_op(self, operand):
        """
        Execute WRITE: Print value at memory[operand].

        Args:
            operand (int): Memory address to read from.
        """
        BasicMLOps.write(self.memory, operand)

    def _handle_load_op(self, operand):
        """
        Execute LOAD: Load value from memory[operand] into accumulator.

        Args:
            operand (int): Memory address to load.
        """
        self.accumulator = BasicMLOps.load(self.memory, operand, self.accumulator)

    def _handle_store_op(self, operand):
        """
        Execute STORE: Store the accumulator into memory[operand].

        Args:
            operand (int): Memory address to store into.
        """
        BasicMLOps.store(self.memory, operand, self.accumulator)

    def _handle_add_op(self, operand):
        """
        Execute ADD: Add value from memory[operand] to accumulator.

        Args:
            operand (int): Memory address to read from.
        """
        self.accumulator = BasicMLOps.add(self.accumulator, self.memory[operand])

    def _handle_subtract_op(self, operand):
        """
        Execute SUBTRACT: Subtract memory[operand] from accumulator.

        Args:
            operand (int): Memory address to read from.
        """
        self.accumulator = BasicMLOps.subtract(self.accumulator, self.memory[operand])

    def _handle_divide_op(self, operand):
        """
        Execute DIVIDE: Divide accumulator by memory[operand].

        Args:
            operand (int): Memory address to read from.
        """
        try:
            self.accumulator = BasicMLOps.divide(self.accumulator, self.memory[operand])
        except ZeroDivisionError as e:
            print(e)
            self.halted = True

    def _handle_multiply_op(self, operand):
        """
        Execute MULTIPLY: Multiply accumulator by memory[operand].

        Args:
            operand (int): Memory address to read from.
        """
        self.accumulator = BasicMLOps.multiply(self.accumulator, self.memory[operand])

    def _handle_branch_op(self, operand):
        """
        Execute BRANCH: Unconditional jump to operand.

        Args:
            operand (int): Target instruction index.
        """
        self.program_counter = BasicMLOps.branch(operand)

    def _handle_branch_neg_op(self, operand):
        """
        Execute BRANCHNEG: Jump to operand if accumulator is negative.

        Args:
            operand (int): Target instruction index.
        """
        self.program_counter = BasicMLOps.branch_neg(self.program_counter, operand, self.accumulator)

    def _handle_branch_zero_op(self, operand):
        """
        Execute BRANCHZERO: Jump to operand if accumulator is zero.

        Args:
            operand (int): Target instruction index.
        """
        self.program_counter = BasicMLOps.branch_zero(self.program_counter, operand, self.accumulator)

    def _handle_halt_op(self, operand):
        """
        Execute HALT: Stop the program.

        Args:
            operand (int): Unused operand.
        """
        BasicMLOps.halt()
        self.halted = True

    def _handle_invalid_op(self, operand):
        """
        Handle an unknown or invalid opcode.

        Args:
            operand (int): Operand that was passed.
        """
        print(f"Unknown instruction at PC {self.program_counter}")
        self.halted = True
