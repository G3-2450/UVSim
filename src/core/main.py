'''
main.py

'''
from .ProgramLoader import ProgramLoader
from .InstructionExecutor import InstructionExecutor
from .MemoryModel import MemoryModel

class UVSimCore:
    def __init__(self, get_input_callback):
        self.memory_model = MemoryModel()
        self.loader = ProgramLoader(self.memory_model)
        self.executor = InstructionExecutor(self.memory_model, get_input_callback)

    def load_program(self, filename):
        return self.loader.load_program(filename)
        
    def run_program(self):
        self.executor.run_program()
