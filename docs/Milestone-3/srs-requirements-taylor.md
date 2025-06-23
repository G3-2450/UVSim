
# Software Requirements Specification (SRS) – UVSim GUI 
---

## Functional Requirements

Each functional requirement is labeled **FR-#** and follows the format:  
**Description, Inputs, Expected Output, Pre/Post Conditions (when relevant).**

### FR-01 – Load Program File
**Description**: The system must allow users to load a `.txt` or `.ml` program file into memory.

### FR-02 – Display Memory Contents
**Description**: The GUI must display all 100 memory locations in a scrollable grid/table.

### FR-03 – Start Program Execution
**Description**: Clicking “Run” executes the loaded program from memory location 00.

### FR-04 – Step-by-Step Execution
**Description**: User can click “Step” to execute one instruction at a time.

### FR-05 – Display Accumulator Value
**Description**: The current value of the accumulator must be shown in the GUI and update in real time.

### FR-06 – Highlight Current Instruction Pointer
**Description**: The memory cell currently being executed must be highlighted in the GUI.

### FR-07 – READ Operation Prompt
- **Description**: On a `READ` instruction (10), the GUI must prompt the user for input via dialog.

### FR-08 – WRITE Operation Output
**Description**: On a `WRITE` instruction (11), the system should display the memory value in an output panel or console section.

### FR-09 – Clear Memory and Registers
**Description**: The system must allow users to clear/reset memory and the accumulator to zero.

### FR-10 – Save Current Program
- **Description**: The system must allow users to export the current memory contents to a `.txt` file.

### FR-11 – Error Detection: Invalid Opcode
**Description**: If a program contains an unknown opcode, execution must stop and an error must be shown.

### FR-12 – Branch Control Flow Execution
**Description**: The simulator must correctly implement `BRANCH`, `BRANCHNEG`, and `BRANCHZERO` instructions.

### FR-13 – Arithmetic Error Handling (e.g., divide by zero)
**Description**: If a divide by zero occurs, halt execution and show a message.

### FR-14 – Instruction Format Validation
**Description**: The system must validate that all loaded memory values are four-digit signed integers.

### FR-15 – Instruction History Log
**Description**: The GUI must maintain a list of executed instructions in order for user review.

---

## Non-Functional Requirements

### NFR-01 – Development Media
The application must be implemented in Python and the front end implemented using Python GUI/Kivy

### NFR-02 – User-Friendly Interface
The GUI should be intuitive, with clearly labeled buttons and consistent layout (e.g., Memory panel, Output console, Input prompt).

### NFR-03 – Performance & Responsiveness
The GUI must respond to user input and file loads within 1 second; step execution should occur in real time with minimal delay.