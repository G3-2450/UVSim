## Use Cases

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
