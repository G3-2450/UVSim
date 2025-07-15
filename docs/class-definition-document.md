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

#### gui.py (interface)
**Initializes and runs the program interface for UVSim, loading visual components from three .kv files and defining the main interface classes used in the application.**

##### Class: LeftPaneWidget()

- Purpose: displays the left pane of the interface including instructions and buttons for interaction (upload, run, step, start over)
- Defined in: LeftPaneWidget.kv, linked to LeftPaneWidget class in main.py
- Functions:
  - __init__(self, **kwargs)
    - Purpose: Initialize the widget and its layout
    - Return: None
    - Preconditions: Kivy will call this automatically
    - Postconditions: The layout is ready for interaction

  - upload_file(self)
    - Purpose: Opens a file chooser popup to select a .txt file
    - Return: None
    - Preconditions: Kivy app is running; file selection popup is needed
    - Postconditions: Popup is shown; user can select a .txt file

  - open_editor_popup (self, file_path)
    - Purpose: Opens a popup for editing the selected .txt file
    - Return: None
    - Preconditions: A valid path to a .txt file must be provided
    - Postconditions: Popup displays file contents for editing and saving

  - save_to_user_program(_) (inner function)
    - Purpose: Saves edited text to user_program.txt, loads it into memory, and populates GUI
    - Return: None
    - Preconditions: File has been opened and user clicked "Save"
    - Postconditions: File saved as user_program.txt; memory GUI is updated

  - cancel_editor_popup(_)
    - Purpose: Dismisses the file editor popup without saving
    - Return: None
    - Preconditions: Editor popup is open
    - Postconditions: Editor popup is closed

  - cancel_file_popup(_)
    - Purpose: Dismisses the file chooser popup
    - Return: None
    - Preconditions: File chooser popup is open
    - Postconditions: File chooser popup is closed
     
  - popuplate_memory(self, root, memory)
    - Purpose: Fills the GUI memory slots with values from a given memory list
    - Return: None
    - Preconditions: memory must be a list of 100 integers; GUI must be built
    - Postconditions: All 100 memory slots in the GUI display the corresponding value

  - run_button(self)
    - Purpose: Loads the user program, populates memory, and runs the program through UVSimCore
    - Return: None
    - Preconditions: user_program.txt must exist; UVSimCore must be initialized
    - Postconditions: Program is executed (possibly requesting input), memory is updated
     
  - step_button(self)
    - Purpose: Executes one instruction via UVSimCore.step() and updates memory and register display
    - Return: None
    - Preconditions: Program must be loaded into CoreInstance; step() should be implemented
    - Postconditions: One instruction is executed; accumulator, program counter, and memory view are updated

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
- Functions:
  - execute_command(self, input)
    - Purpose: Handles when the user presses Enter in the console; calls a stored input callback
    - Return: None
    - Preconditions: A CallbackFunction must be set via get_input()
    - Postconditions: Callback is triggered with input; text field is cleared and disabled

  - add_message(self, text=None)
    - Purpose: Adds a new line of text to the scrollable console display
    - Return: None
    - Preconditions: text must not be None
    - Postconditions: Console text updated; view scrolls to bottom

  - _scroll_to_bottom(self, *args)
    - Purpose: Scrolls the console output to the most recent line
    - Return: None
    - Preconditions: Should be scheduled by Clock.schedule_once(...)
    - Postconditions: Console is scrolled fully down

  - get_input(self, prompText="Enter value: ", InputFunction=None)
    - Purpose: Enables the console input and registers a callback for when Enter is pressed
    - Return: None
    - Preconditions: A valid callable must be passed as InputFunction
    - Postconditions: Console input is enabled and waiting for user input
    
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

  - _setup_console_redirect(self, dt)
    - Purpose: Redirects sys.stdout to the GUI console and initializes UVSimCore
    - Return: None
    - Preconditions: The GUI must be fully initialized
    - Postconditions: print() now writes to GUI; CoreInstance is available
