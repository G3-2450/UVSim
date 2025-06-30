## Non-Functional Requirements

### Design
- The application must be implemented in Python and the front end implemented using Python GUI/Kivy
- UVSim should show all memory addresses without needing multiple pages

### Performance & Responsiveness
- UVSim should be able to launch within 3 seconds and the GUI must respond to user input and file loads within 1 second.

### Reliability
- UVSim should not crash when a incorrect file type is provided
- Works fully offline


## Functional Requirements

### FR-01 – Load Program File
**Description**: The system must allow users to read, write, load, and parse a `.txt` or `.ml` program file into memory.

### FR-02 – Halt Program
**Description**: On instruction (10) or end of file, halt program.

### FR-03 – Start Program Execution
**Description**: Clicking “Run” executes the loaded program from memory location 00.

### FR-04 – Step-by-Step Execution
**Description**: User can click “Step” to execute one instruction at a time.

### FR-05 – Display Accumulator Value
**Description**: The current value of the accumulator must be shown in the GUI and update in real time.

### FR-06 – Highlight Current Instruction Pointer
**Description**: The memory cell currently being executed must be highlighted in the GUI.

### FR-07 – READ Operation Prompt
- **Description**: On a `READ` instruction (10), the GUI must prompt the user for input in the console.

### FR-08 – WRITE Operation Output
**Description**: On a `WRITE` instruction (11), the system should display the memory value in an console section.

### FR-09 – Clear Memory and Registers
**Description**: The system must allow users to clear/reset memory and the accumulator to zero.

### FR-11 – Error Detection: Invalid Opcode
**Description**: If a program contains an unknown opcode, execution must stop and an error must be shown.

### FR-12 – Branch Control Flow Execution
**Description**: The simulator must correctly implement `BRANCH`, `BRANCHNEG`, and `BRANCHZERO` instructions.

### FR-13 – Arithmetic Error Handling (e.g., divide by zero)
**Description**: If a divide by zero occurs, halt execution and show a message.

### FR-14 – Instruction Format Validation
**Description**: The system must validate that all loaded memory values are four-digit signed integers.

### FR-15 – Highlight Instruction
**Description**: Highlight current instruction

### FR-16 – Arithmetic Instruction
**Description**: The system must be able to add, subtract, divide, and multiply values on op codes (30), (31), (32), (33), respectively

### FR-16 – Store Instruction
**Description**: On op code (21), store the value from the accumulator to the designated memory location.

