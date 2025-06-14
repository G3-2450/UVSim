## User Stories
As a computer science student, I want to load and run machine language programs using a virtual simulator, so that I can better understand how CPUs execute instructions at the lowest level.

As a user, I want to provide input and see output as my program runs, so that I can verify that my code logic and data handling are working correctly.


## Use Cases

##### READ
Actor → Student
System → Program reaches a READ instruction and prompts for user input → Student enters a number → System stores the value in the specified memory location
Goal → Student provides input during execution, allowing the program to operate dynamically based on that input.

##### WRITE
Actor → Student
System → Program reaches a WRITE instruction and retrieves the value from the specified memory location → System prints the value to the console
Goal → Student views the result of data stored or processed during execution, verifying correct behavior of the program.

##### LOAD
Actor -> Student
System -> Enters a LOAD instruction and retrieves the value from the specified memory location -> System stores the value in the accumulator
Goal -> Student loads a value into the accumulator for future arithmetic or logical operations

##### STORE
Actor -> Student
System -> Enters a STORE instruction and takes the current value in the accumulator -> System writes that value into the specified memory location
Goal -> Student saves the accumulator value for later use or reference during program execution

##### ADD
Actor -> Student
System -> Enters a ADD instruction and retrieves the value from the specified memory location -> System adds that value to the accumulator and updates the accumulator with the result
Goal -> Student performs addition with a value in memory and stores the result for continued computation

##### SUBTRACT
Actor -> Student
System -> Enters a SUBTRACT instruction and retrieves the value from the specified memory location -> System subtracts that value from the accumulator and updates the accumulator with the result
Goal -> Student performs subtraction and prepares the accumulator for further instructions based on the result

##### DIVIDE
Actor -> Student
System -> Enters a DIVIDE instruction and retrieves the value from the specified memory location -> System divides the accumulator by that value and updates the accumulator with the result (if non-zero)
Goal -> Student performs division and obtains a new value in the accumulator based on program logic

##### MULTIPLY
Actor -> Student
System -> Enters a MULTIPLY instruction and retrieves the value from the specified memory location -> System multiplies it with the accumulator and stores the result in the accumulator
Goal -> Student multiplies values during execution to compute or transform data for use in the program

##### BRANCH  
Actor -> Student  
system -> the BRANCH command in UVSim.  
goal -> navigate to a specified location in the program.  
  
##### BRANCHNEG  
Actor -> Student  
system -> the BRANCHNEG command in UVSim.  
goal -> navigate to a specified location in the program if the last operation resulted in a negative number.  
  
##### BRANCHZERO  
Actor -> Student  
system -> the BRANCHZERO command in UVSim.  
goal -> navigate to a specified location in the program if the last operation resulted in a zero.  
  
##### HALT  
Actor -> Student  
system -> the HALT command in UVSim.  
goal -> Stop the program.  