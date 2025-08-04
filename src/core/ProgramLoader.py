class ProgramLoader:
    """
    Loads a BasicML program from a file into the UVSim memory model.
    Supports both 4-digit (+1007) and 6-digit (+010007) instruction formats.
    """

    def __init__(self, memory_model):
        """
        Initializes the ProgramLoader with a reference to the memory model.

        Args:
            memory_model (MemoryModel): The memory model used to store program instructions.
        """
        self.memory_model = memory_model

    def convert_to_6_digit(self, content_lines):
        """
        Converts 4-digit instructions to 6-digit format.

        Format conversion:
            From: +1007 (4-digit: sign + opcode + operand)
            To:   +010007 (6-digit: sign + 3-digit opcode + 3-digit operand)

        Args:
            content_lines (list of str): Lines read from the program file.

        Returns:
            list of str: Converted lines in 6-digit format.

        Raises:
            ValueError: If any line is invalid.
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
            opcode = line[1:3]          # two-digit opcode
            operand = line[3:]          # two-digit operand
            new_word = f"{sign}0{opcode}0{operand}"
            converted.append(new_word)
        return converted

    def load_program(self, filename):
        """
        Loads a program from a file into memory.

        Automatically detects whether the file uses 4-digit or 6-digit format.
        Resets memory before loading.

        Args:
            filename (str): Path to the program file.

        Returns:
            list or None: Memory after loading program, or None if error occurs.

        Raises:
            ValueError: If the file contains invalid or mixed instruction formats.
        """
        self.memory_model.reset()

        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]

            if len(lines) > 250:
                raise ValueError("Program has more than 250 lines.")

            if all(len(line) == 5 for line in lines):  # 4-digit format
                print("Detected 4-digit file. Converting to 6-digit format...")
                lines = self.convert_to_6_digit(lines)

            elif not all(len(line) == 7 for line in lines):  # 6-digit format
                raise ValueError("Mixed or invalid instruction format detected.")

            for i, line in enumerate(lines):
                if not (line.startswith('+') or line.startswith('-')):
                    raise ValueError(f"Invalid format at line {i + 1}: {line}")
                self.memory_model.memory[i] = int(line)

        except FileNotFoundError:
            print("Error: File not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None

        return self.memory_model.memory
