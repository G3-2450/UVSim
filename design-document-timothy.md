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