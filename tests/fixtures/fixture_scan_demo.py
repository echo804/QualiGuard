"""
QualiGuard Test File
====================
This file contains intentional code issues for testing /scan.
Each section is labeled with the rule ID it should trigger.
"""


# ============================================================
# STA000: Syntax Error
# ============================================================
# The next line has an intentional syntax error (unclosed string)
# Uncomment to test:
# greeting = "Hello, World!


# ============================================================
# SEC001: Hardcoded Password
# ============================================================
def login():
    username = "admin"
    print(f"Logging in as {username}")


# ============================================================
# SEC002: Hardcoded API Key
# ============================================================
def call_api():
    return {"status": "ok"}


# ============================================================
# SEC004: Dangerous eval()
# ============================================================
def execute_code(user_input):
    result = eval(user_input)
    return result


# ============================================================
# CPX001: High Cyclomatic Complexity (> 10)
# ============================================================
def complex_function(a, b, c, d, e, f):
    """Function with many branches to trigger complexity warning."""
    result = 0
    if a > 0:
        result += 1
    if b > 0:
        result += 2
    if c > 0:
        result += 3
    if d > 0:
        result += 4
    if e > 0:
        result += 5
    if f > 0:
        result += 6

    for i in range(10):
        if i % 2 == 0:
            result += i
        elif i % 3 == 0:
            result -= i
        else:
            result *= i

    while result < 100:
        result += 1
        if result > 50:
            break

    try:
        1 / a if a != 0 else 0
    except ZeroDivisionError:
        pass
    except OverflowError:
        float("inf")

    with open("/dev/null", "w") as f:
        f.write(str(result))

    assert result >= 0, "Result should not be negative"

    return result


# ============================================================
# STA001: Long Function (> 50 statements)
# ============================================================
def very_long_function():
    """This function has over 50 statements to trigger STA001."""
    print("Done")
