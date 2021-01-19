from random import randint
from numpy import zeros, roots
import matplotlib.pyplot as plt


class Poly:
    def __init__(self, value, code=None):
        self.coefficients = {}
        self.code = code
        if value is not None:
            assert type(value) == str
            power, coefficient = self.extract(value)
            self.coefficients[power] = coefficient
        return

    def compute(self, value):
        return sum(
            self.coefficients[key] * (value ** key) for key in self.coefficients
        )

    def __str__(self):
        return f"Poly Object of coefficients {self.coefficients}"

    def __add__(self, other):
        assert type(other) == Poly
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] += other.coefficients[key]
            else:
                self.coefficients[key] = other.coefficients[key]
        return self

    def __sub__(self, other):
        assert type(other) == Poly
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] -= other.coefficients[key]
            else:
                self.coefficients[key] = -other.coefficients[key]
        return self

    def __mul__(self, other):
        assert type(other) == Poly
        new = {}
        for okey in other.coefficients:
            for skey in self.coefficients:
                power = okey + skey
                co = other.coefficients[okey] * self.coefficients[skey]
                if power in new:
                    new[power] += co
                else:
                    new[power] = co
        self.coefficients = new
        return self

    def __truediv__(self, other):
        assert type(other) == Poly
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] /= other.coefficients[key]
        return self

    def __pow__(self, power, modulo=None):
        temp = Poly.copy(self)
        out = self
        for _ in range(int(power.coefficients[0]) - 1):
            out = out * temp
        return out

    @staticmethod
    def extract(value):
        power = 0
        coefficient = ""
        new_power = None
        for i, char in enumerate(str(value)):
            if char.isdigit() or char == "." or char == "-":
                if new_power is None:
                    coefficient += char
            elif char == "^":
                new_power = float(value[i + 1])
            elif char not in [" ", ""]:
                # todo: add compatibility for higher powers
                power = 1
        try:
            coefficient = float(coefficient)
        except ValueError:
            if power == 1:
                coefficient = 1.0
            else:
                print("power", power)
                print("value", value)
                raise Exception("AAAAAAAAA")
        if new_power is not None:
            power = new_power
        return power, coefficient

    def merge(self, other):
        assert type(other) == Poly
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] -= other.coefficients[key]
            else:
                self.coefficients[key] = -other.coefficients[key]
        return self

    def tidy_roots(self, roots):
        new_roots = []
        for root in roots:
            if root not in new_roots:
                new_root = root
                if int(new_root) == float(new_root):
                    new_root = int(new_root)
                if -new_root == new_root:
                    new_roots = abs(new_root)
                new_roots.append(new_root)
        if len(new_roots) == 1:
            return new_roots[0]
        return new_roots



    def solve(self):
        if len(self.coefficients) == 1:
            return self.coefficients[0]
        poly = zeros(shape=int(max(self.coefficients) + 1))
        for key in self.coefficients:
            key = int(key)
            poly[key] = self.coefficients[key]
        return self.tidy_roots(roots(poly[::-1]))

    @classmethod
    def copy(cls, other):
        new = cls(None)
        for key in other.coefficients:
            new.coefficients[key] = other.coefficients[key]
        return new

    def derive(self):
        new = {
            key - 1: self.coefficients[key] * key
            for key in self.coefficients
            if key > 0
        }
        self.coefficients = new
        return

    pass


class Equation_Solver:
    polys = {}
    actions = ["^", "*", "/", "+", "-"]

    @staticmethod
    def print_sides(desc, left, right):
        print(desc, left + " = " + right)
        return

    @staticmethod
    def dense(exp):
        return "".join(char for char in exp if char != " ")

    @staticmethod
    def remove_multiple_spaces(exp):
        out = ""
        space = False
        for char in exp:
            if char == " ":
                if not space:
                    space = True
                    out += char
                else:
                    space = False
            else:
                space = False
                out += char
        return out

    def space(self, exp):
        out = " "
        current = ""
        for i, char in enumerate(exp):
            if char == "-":
                if i == 0 or exp[i - 1] in self.actions:
                    current += char
                else:
                    out += " " + current + " " + char + " "
                    current = ""
            elif char not in self.actions:
                current += char
            else:
                out += current + " " + char + " "
                current = ""
        out += current + " "
        spaced = ""
        for char in out:
            if char == "(":
                spaced += " ( "
            elif char == ")":
                spaced += " ) "
            else:
                spaced += char
        spaced = self.remove_multiple_spaces(spaced)
        return spaced

    def not_clean(self, exp):
        return exp.strip() not in self.polys

    def find_index(self, exp):
        target = None
        for act in self.actions:
            if act in exp:
                target = act
                break
        if target is None:
            return -5
        for i, char in enumerate(exp):
            if char == target:
                return i

    def generate_Poly(self, value):
        num = randint(10000, 99999)
        code = "".join(chr(ord("A") + int(n)) for n in str(num))
        while code in self.polys:
            num = randint(10000, 99999)
            code = "".join(chr(ord("A") + int(n)) for n in str(num))
        self.polys[code] = Poly(value, code)
        return code

    @staticmethod
    def bracket_in_exp(exp):
        return "(" in exp or ")" in exp

    @staticmethod
    def find_bracket(exp):
        count = -1
        start = 0
        for i, char in enumerate(exp):
            if char == "(":
                if count == -1:
                    count = 1
                else:
                    count += 1
                start = i
            elif char == ")":
                count -= 1
            if count == 0:
                return start, i

    def remove_brackets(self, exp):
        while self.bracket_in_exp(exp):
            start, end = self.find_bracket(exp)
            inside = exp[start + 1:end]
            cleaned_inside = self.clean(inside)
            exp = exp[:start] + cleaned_inside + exp[end + 1:]
        exp = self.remove_multiple_spaces(exp) + " "
        return exp

    def clean(self, exp):
        if self.bracket_in_exp(exp):
            exp = self.remove_brackets(exp)
        index = self.find_index(exp)
        left = index - 1
        while exp[left] != " ":
            left -= 1
        right = index + 1
        try:
            while right + 1 != len(exp) or exp[right + 1] != " ":
                right += 1
        except IndexError:
            print("INDEXXXX")
            self.print_polys()
            print(right)
            print(exp)
            print(index)
            print(exp[index])
            raise Exception("AAAAAAAAA")
        spliced = exp[left:right].strip().split(" ")
        try:
            a, action, b = spliced
        except ValueError:
            print("SPLIT !")
            print(exp)
            print(exp[left:right])
            print(index)
            print(spliced)
            self.print_polys()
            raise Exception("AAAAAAAAA")
        try:
            a = self.polys[a]
            b = self.polys[b]
        except KeyError:
            print(a)
            print(b)
            print(self.polys)
            print(spliced)
            print(exp)
            raise Exception("AAAAAAAAA")
        if action == "+":
            res = a + b
        elif action == "-":
            res = a - b
        elif action == "*":
            res = a * b
        elif action == "/":
            res = a / b
        elif action == "^":
            res = a ** b
        else:
            raise Exception("AAAAAAAAA")
        exp = " " + exp[:left] + res.code + exp[right:]
        return exp

    def get_calc(self, exp):
        while self.not_clean(exp):
            exp = self.clean(exp)
            if not self.not_clean(exp):
                return exp
        return exp

    def get_sides(self, left, right):
        if type(left) != Poly:
            left = self.polys[left]
        if type(right) != Poly:
            right = self.polys[right]
        return left, right

    def cast(self, exp):
        casted = ""
        objs = exp.strip().split(" ")
        for i, value in enumerate(objs):
            casted += " "
            if value not in self.actions and value not in ["(", ")"]:
                code = self.generate_Poly(value)
                casted += code
                if i + 1 < len(objs) and objs[i + 1] == "(":
                    casted += " * "
            else:
                casted += value
        return casted

    def print_polys(self):
        for key in self.polys:
            print(f"{key} - {str(self.polys[key])}")
        return

    def to_poly(self, eq):
        left, right = eq.split("=") if "=" in eq else (eq, "0")
        dense_left, dense_right = self.dense(left), self.dense(right)
        spaced_left, spaced_right = self.space(dense_left), self.space(dense_right)
        poly_left, poly_right = self.cast(spaced_left), self.cast(spaced_right)
        calc_left, calc_right = self.get_calc(poly_left).strip(), self.get_calc(poly_right).strip()
        return self.polys[calc_left], self.polys[calc_right]

    pass


class Graph:
    def __init__(self, eq):
        solver = Equation_Solver()
        self.eq = solver.to_poly(eq)[0]
        return

    def get_derivative(self):
        self.eq.derive()
        return self


def solve(eq):
    solver = Equation_Solver()
    poly_left, poly_right = solver.to_poly(eq)
    merged_poly = poly_left.merge(poly_right)
    return merged_poly.solve()
