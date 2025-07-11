import sys

class WriteToGuiConsole:
    def __init__(self, add_message_func):
        self.add_message_func = add_message_func
        self.buffer = ""

    def write(self, s):
        # print() passes in s
        self.buffer += s
        if '\n' in self.buffer:
            lines = self.buffer.split('\n')
            for line in lines[:-1]: # Prints all complete lines
                self.add_message_func(line)
            self.buffer = lines[-1] # Holds onto any partial line

    def flush(self):
        # prints buffered content
        if self.buffer:
            self.add_message_func(self.buffer)
            self.buffer = ""