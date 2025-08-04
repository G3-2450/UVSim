from core.BasicMLOps import BasicMLOps
from kivy.clock import Clock

class InstructionExecutor:
    """
    Executes BasicML program instructions stored in memory, one step at a time.
    Handles control flow, arithmetic operations, input/output, and memory access.
    """

    def __init__(self, memory_model, get_input_callback):
        """
        Initializes the executor with the memory model and input callback.

        Args:
            memory_model (MemoryModel): The shared memory and register model.
            get_input_callback (Callable): Function to request input asynchronously.
        """
        self.memory_model = memory_model
        self.get_input = get_input_callback

    def run_program(self):
        """
        Begins scheduled execution of the program by stepping through instructions at intervals.
        """
        Clock.schedule_interval(self._run_step, 0.1)

    def _run_step(self, dt):
        """
        Executes a single instruction per scheduled interval tick.

        Args:
            dt (float): Time delta from the Kivy clock scheduler.
        """
        if self.memory_model.halted or self.memory_model.program_counter >= len(self.memory_model.memory):
            return False  # Stop scheduling
        self.step()

    def step(self):
        """
        Executes a single instruction at the current program counter.

        Handles parsing and dispatching the opcode to the correct operation.
        """
        if self.memory_model.halted or self.memory_model.program_counter >= len(self.memory_model.memory):
            print("Program Halted or out of bounds")
            return

        instruction = self.memory_model.memory[self.memory_model.program_counter]
        opcode = abs(instruction) // 1000     # First 3 digits
        operand = abs(instruction) % 1000     # Last 3 digits

        if operand < 0 or operand > 249:
            print(f"Invalid memory access at line {self.memory_model.program_counter}: {operand}")
            self.memory_model.halted = True
            return

        if opcode == 10:
            # READ: Prompt user to input a value to memory[operand]
            self.get_input(f"READ to memory [{operand}]:", lambda value: self._handle_read(operand, value))
            return
        elif opcode == 11:
            # WRITE: Output the value at memory[operand]
            BasicMLOps.write(self.memory_model.memory, operand)
        elif opcode == 20:
            # LOAD: Load value from memory[operand] into accumulator
            self.memory_model.accumulator = BasicMLOps.load(
                self.memory_model.memory, operand, self.memory_model.accumulator)
        elif opcode == 21:
            # STORE: Store value from accumulator into memory[operand]
            BasicMLOps.store(self.memory_model.memory, operand, self.memory_model.accumulator)
        elif opcode == 30:
            # ADD: Add memory[operand] to accumulator
            self.memory_model.accumulator = BasicMLOps.add(
                self.memory_model.accumulator, self.memory_model.memory[operand])
        elif opcode == 31:
            # SUBTRACT: Subtract memory[operand] from accumulator
            self.memory_model.accumulator = BasicMLOps.subtract(
                self.memory_model.accumulator, self.memory_model.memory[operand])
        elif opcode == 32:
            # DIVIDE: Divide accumulator by memory[operand]
            try:
                self.memory_model.accumulator = BasicMLOps.divide(
                    self.memory_model.accumulator, self.memory_model.memory[operand])
            except ZeroDivisionError as e:
                print(e)
                self.memory_model.halted = True
                return
        elif opcode == 33:
            # MULTIPLY: Multiply accumulator by memory[operand]
            self.memory_model.accumulator = BasicMLOps.multiply(
                self.memory_model.accumulator, self.memory_model.memory[operand])
        elif opcode == 40:
            # BRANCH: Jump to address
            self.memory_model.program_counter = BasicMLOps.branch(operand)
            return
        elif opcode == 41:
            # BRANCHNEG: Jump if accumulator is negative
            self.memory_model.program_counter = BasicMLOps.branch_neg(
                self.memory_model.program_counter, operand, self.memory_model.accumulator)
            return
        elif opcode == 42:
            # BRANCHZERO: Jump if accumulator is zero
            self.memory_model.program_counter = BasicMLOps.branch_zero(
                self.memory_model.program_counter, operand, self.memory_model.accumulator)
            return
        elif opcode == 43:
            # HALT: Stop program
            BasicMLOps.halt()
            self.memory_model.halted = True
            return
        else:
            print(f"Unknown instruction: {instruction}")
            self.memory_model.halted = True
            return

        # Move to next instruction unless a branch or halt occurred
        self.memory_model.program_counter += 1

    def _handle_read(self, address, value):
        """
        Handles user input after a READ instruction.

        Args:
            address (int): Memory location to store input.
            value (str): Input string to be parsed and stored.
        """
        try:
            self.memory_model.memory[address] = int(value)
            self.memory_model.program_counter += 1
        except ValueError:
            print("Invalid input. Please enter an integer.")
