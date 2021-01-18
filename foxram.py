from equation_solver import to_poly
from numpy import roots


class Foxram:
    @staticmethod
    def solve(eq):
        poly_left, poly_right = to_poly(eq)
        print(poly_right)
        print(poly_left)
        exit()
        merged_poly = poly_left.merge(poly_right)
        return merged_poly.solve()
