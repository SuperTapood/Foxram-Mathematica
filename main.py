from time import time_ns as time
from foxram import *


def test(eq, act):
    start = time()
    pred = solve(eq)
    end = time() - start
    end = f'{end:,}'
    try:
        assert pred == act
    except AssertionError:
        raise Exception(f"Test case failed in {end}ns.\n"
                        f" Got equation {eq}\n"
                        f" and got {pred} instead of {act}")
    print(f"The algorithm solved the equation: {eq}\n"
          f"and got {pred} in {end}ns")
    return


solve("-5(x + 5)^2 = 0")
solve("2x + 5 + 100x - 3 - 3x - 10 = 18 * x")
