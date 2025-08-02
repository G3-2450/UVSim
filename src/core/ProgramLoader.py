'''
Loads the progarm
Converts 4bit files to 6bit files

'''

class ProgramLoader:
    def __init__(self, memory_model):
        self.memory_model = memory_model

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
        self.memory_model.reset()

        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]

            if len(lines) > 250:
                raise ValueError("Program has more than 250 lines.")

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
                self.memory_model.memory[i] = int(line)

        except FileNotFoundError:
            print("Error: File not found.")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None

        return self.memory_model.memory
    