from BasicMLOps import BasicMLOps
from unittest.mock import patch

# READ was moved out of BasicMLOps

# --- READ Tests ---
# def test_read_valid_input():
#     memory = [0] * 100
#     with patch('builtins.input', return_value='42'):
#         BasicMLOps.read(memory, 7)
#     if memory[7] != 42:
#         raise Exception("READ valid input failed")

# def test_read_invalid_then_valid_input():
#     memory = [0] * 100
#     with patch('builtins.input', side_effect=['abc', '15']):
#         BasicMLOps.read(memory, 5)
#     if memory[5] != 15:
#         raise Exception("READ invalid then valid input failed")

# --- WRITE Tests ---
def test_write_output():
    memory = [0] * 100
    memory[3] = 99
    with patch('builtins.print') as mock_print:
        BasicMLOps.write(memory, 3)
        if mock_print.call_args[0][0] != "WRITE from memory[3]: 99":
            raise Exception("WRITE output failed")

def test_write_empty_slot():
    memory = [0] * 100
    with patch('builtins.print') as mock_print:
        BasicMLOps.write(memory, 4)
        if mock_print.call_args[0][0] != "WRITE from memory[4]: 0":
            raise Exception("WRITE empty slot failed")

# --- LOAD Tests ---
def test_load_value():
    memory = [0] * 100
    memory[2] = 25
    result = BasicMLOps.load(memory, 2, 0)
    if result != 25:
        raise Exception("LOAD value failed")

def test_load_negative():
    memory = [0] * 100
    memory[8] = -13
    result = BasicMLOps.load(memory, 8, 0)
    if result != -13:
        raise Exception("LOAD negative value failed")

# --- STORE Tests ---
def test_store_positive():
    memory = [0] * 100
    accumulator = 45
    BasicMLOps.store(memory, 10, accumulator)
    if memory[10] != 45:
        raise Exception("STORE positive value failed")

def test_store_negative():
    memory = [0] * 100
    accumulator = -17
    BasicMLOps.store(memory, 22, accumulator)
    if memory[22] != -17:
        raise Exception("STORE negative value failed")

# --- Custom Dot-Style Test Runner ---
if __name__ == '__main__':
    tests = [
        # test_read_valid_input,
        # test_read_invalid_then_valid_input,
        test_write_output,
        test_write_empty_slot,
        test_load_value,
        test_load_negative,
        test_store_positive,
        test_store_negative
    ]

    failures = 0

    for test in tests:
        try:
            test()
            print('.', end='', flush=True)
        except Exception as e:
            print('F', end='', flush=True)
            failures += 1

    print()  # new line
    if failures == 0:
        print("All tests passed ✅")
    else:
        print(f"{failures} test(s) failed ❌")
        
print(f"\nTotal tests run: {len(tests)}")
