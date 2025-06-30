                                              Class Definition Document

#### BasicMLOps.py
##### Class: BasicMLOps()
##### Purpose: 
Handles all basic ML operations, categorized into input/output operations, load/store operations, arithmetic operations and control flow operations. This class serves as the backend logic for executing commands.

##### Functions:
**read(memory, address):** 
- Purpose: prompts for user input and stores the value at a memory address
- Parameters: 
    - memory(list): simulated memory
    - address(int): target memory index
- Return: None
- Pre-condition: address is a valid index in memory
- Post-condition: memory[address] updated with user input

**write(memory, address):**
- Purpose: prints value at memory address
- Parameters:
    - memory(list)
    - address(int)
- Return: None
- Pre-condition: memory address is valid
- Post-condition: value is displayed in console

**load(memory, address, accumulator):
- Purpose: loads value from memory into the accumulator
- Parameters:
    - memory(list)
    - address(int)
    - accumulator(int)
- Return: new accumulator value
- Pre-condition: memory address is valid
- Post-condition: value loaded into accumulator

**store(memory, address, accumulator):**
- Purpose: stores the current accumulator value into memory
- Parameters:
    - memory(list)
    - address(int)
    - accumulator(int)
- Return: None
- Pre-condition: 
    -  memory should be a valid list of integers of pre-determined size
    - accumulator should contain a valid integer to store
- Post-condition: memory[address] is updated and reflects the accumulator value

**add, subtract, divide, multiply:**
- Purpose: perform arithmetic operation
- Parameters:
    - accumulator(int)
    - memory_value(int)
- Return: result of the operation
- Pre-condition: memory_value is valid (falls within pre-determined memory size)
- Post-condition: result is calculated and returned as a valid integer

**branch(nextProgramCounter):**
- Purpose: unconditionally jump to a new memory address(line of code)
- Parameters:
    - nextProgramCounter(int): the memory address to branch to
- Return: the nextProgramCounter value
- Pre-condition: nextProgramCounter must be a non-negative integer within the bounds of memory
- Post-condition: program counter is updated to new memory address

**branch_neg(currentProgramCounter, nextProgramCounter, accumulator):**
- Purpose: branch to the nextProgramCounter if the accumulator is a negative value, otherwise, continue to the next instruction
- Parameters:
    - currentProgramCounter(int): current instruction index
    - nextProgramCounter(int): the target address to branch to if condition is met
    - accumulator(int): current value in the accumulator
- Return: nextProgramCounter or currentProgramCounter + 1
- Pre-condition:
    - currentProgramCounter >= 0
    - nextProgramCounter is a valid address if accumulator < 0
- Post-condition: correct instruction is executed, if accumulator < 0, jump occurs, otherwise currentProgramCounter + 1

**branch_zero(currentProgramCounter, nextProgramCounter, accumulator):**
- Purpose: branch to nextProgramCounter if accumulator = 0, otherwise, continue to the next instruction
- Parameters:
    - currentProgramCounter(int): current instruction index
    - nextProgramCounter(int): the target address to branch to if condition is met
    - accumulator(int): current value in the accumulator
- Return: nextProgramCounter or currentProgramCounter + 1
- Pre-condition:
    - currentProgramCounter >= 0
    - nextProgramCounter is a valid address if accumulator == 0
- Post-condition: correct instruction is executed, if accumulator == 0, jump occurs, otherwise currentProgramCounter + 1

**halt():**
- Purpose: halts program execution
- Return: None
- Post-condition: program is halted  

---
#### main.py

**Contains procedural logic to run the program.**

##### Functions:

**load_program(filename)
- Purpose: reads a basic ML file into memory
- Parameters:
    - filename(str): name of the file being loaded into memory
- Return: list[int] memory
- Pre-condition: file exists and is formatted correctly
- Post-condition: file is loaded into memory

**run_program(memory):**
- Purpose: parses and executes instructions from memory
- Parameters:
    - memory(list[int])
- Return: None
- Pre-condition: valid instructions in memory
- Post-condition: program executes or halts

**main():**
- Purpose: entry point for Command Line Interference (CLI)
- Pre-condition: user provides a valid file name
- Post-condition: the program executes or exits

---

#### main.py (interface)
**Initializes and runs the program interface for UVSim, loading visual components from three .kv files and defining the main interface classes used in the application.**

##### Class: LeftPaneWidget()

- Purpose: displays the left pane of the interface including instructions and buttons for interaction (upload, run, step, start over)
- Defined in: LeftPaneWidget.kv, linked to LeftPaneWidget class in main.py
- Functions: none defined in Python for now, all interactions are defined visually in .kv file
- Pre-Conditions: UI must be loaded using Builder.load_file('LeftPaneWidget.kv')
- Post-Conditions: the widget renders in the left pane and allows interaction through buttons

##### Class: MemRegWidget()

- Purpose: Handles the visual display of the accumulator, program counter, and memory slots from address 00 to 99.
- Defined in: MemRegWidget.kv, logic in main.py
- Functions:
    - on_kv_post(self, base_widget)
        - Purpose: called after the widget is fully initialized; triggers population of the memory display
        - Parameters: base_widget – root of the UI tree
        - Returns: None.
        - Pre-Conditions: widget must be loaded via .kv file and instantiated
        - Post-Conditions: calls populate_memory() to add memory rows to the UI
        
    - populate_memory(self)
        - Purpose: dynamically populates the memory view with 100 labeled TextInput fields for addresses 00–99.
        - Parameters: none
        - Returns: none
        - Pre-Conditions: memory_box ID must be defined in MemRegWidget.kv
        - Post-Conditions: memory display box is populated with scrollable memory entries

##### Class: ConsoleWidget()

- Purpose: manages user command input and output display (scrollable console output and command entry).
- Defined in: ConsoleWidget.kv, linked to ConsoleWidget class in main.py.
- Functions: none implemented in Python yet
- Pre-Conditions: UI must be loaded using Builder.load_file('ConsoleWidget.kv')
- Post-Conditions: the widget renders in the right pane displaying the console

##### Class: UVSimWindow()

- Purpose: master layout container for the full UVSim interface — left and right panes (which contain all sub-widgets)
- Defined in: uvsim.kv, Python class defined in main.py
- Functions: none
- Pre-Conditions: used as root widget in UVSimApp
- Post-Conditions: complete layout is rendered when app is launched

##### Class: UVSimApp()

- Purpose: Entry point for the Kivy application. Initializes the window and loads the root layout UVSimWindow.
- Defined in: main.py
- Functions:
    - build(self)
        - Purpose: instantiates and returns the root UI widget
        - Parameters: none
        - Returns: UVSimWindow instance
        - Pre-Conditions: called automatically by Kivy
        - Post-Conditions: application window opens with full interface



