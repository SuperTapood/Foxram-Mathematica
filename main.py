from time import time_ns
from foxram import *


def test(eq, act):
    start = time_ns()
    pred = solve(eq)
    end = time_ns() - start
    try:
        assert pred == act
    except AssertionError:
        raise Exception(f"Test case failed in {end}ns.\n"
                        f" Got equation {eq}\n"
                        f" and got {pred} instead of {act}")
    print(f"Test case success in {end}ns")
    return


print(solve("-5(x + 5)^2 = 0"))
