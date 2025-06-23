'''
CS 2450 - Final Group Project - UVUSim
Milestone 2: Working Prototype Functions 
Arithmetic Operations (ADD, SUBTRACT, DIVIDE, and MULTIPLY)
'''

#Arithmetic operation:
#ADD = 30 Add a word from a specific location in memory to the 
#    word in the accumulator (leave the result in the accumulator)
#SUBTRACT = 31 Subtract a word from a specific location in 
#    memory from the word in the accumulator (leave the result in the accumulator)
#DIVIDE = 32 Divide the word in the accumulator by a word from 
#    a specific location in memory (leave the result in the accumulator).
#MULTIPLY = 33 multiply a word from a specific location in 
#    memory to the word in the accumulator (leave the result in the accumulator).


def ADD(accumulator, memory_value):
    print(f"ADD: {accumulator} + {memory_value}")
    return accumulator + memory_value

def SUBTRACT(accumulator, memory_value):
    print(f"SUBTRACT: {accumulator} - {memory_value}")
    return accumulator - memory_value

def DIVIDE(accumulator, memory_value):
    if memory_value == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    print(f"DIVIDE: {accumulator} // {memory_value}")
    return accumulator // memory_value

def MULTIPLY(accumulator, memory_value):
    print(f"MULTIPLY: {accumulator} * {memory_value}")
    return accumulator * memory_value
