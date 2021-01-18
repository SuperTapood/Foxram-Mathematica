from time import time_ns
from foxram import Foxram


def test(eq, act):
    start = time_ns()
    pred = Foxram().solve(eq)
    end = time_ns() - start
    try:
        assert pred == act
    except AssertionError:
        raise Exception(f"Test case failed in {end}ns.\n"
                        f" Got equation {eq}\n"
                        f" and got {pred} instead of {act}")
    print(f"Test case success in {end}ns")
    return


# test("3+5", 8.0)
# test("4-5", -1.0)
# test("3/5", 0.6)
# test("3*-6", -18.0)
# test("3 * 8 + -3 * 96 + 51 / 3", -247.0)
print(Foxram.solve("2x + 5 + 100x - 3 - 3x - 10 = 18*x"))
