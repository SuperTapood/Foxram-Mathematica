from random import randint

from Calc_old import *
from numpy import roots


class Foxram:
    actions = ["*", "/", "+", "-"]
    calcs = {}

    def space(self, eq):
        out = " "
        current = ""
        for char in eq:
            if char != " ":
                if char == "-" or char not in self.actions:
                    current += char
                else:
                    current += " " + char + " "
                    out += current
                    current = ""
        current += " "
        out += current
        return out

    def get_calc(self, a, act, b):
        code = str(randint(100000, 999999))
        code = "".join(chr(ord("A") + int(c)) for c in code)
        assert code not in self.calcs
        if act == "+":
            self.calcs[code] = Add(a, b, code)
        elif act == "-":
            self.calcs[code] = Sub(a, b, code)
        elif act == "*":
            self.calcs[code] = Mult(a, b, code)
        elif act == "/":
            self.calcs[code] = Div(a, b, code)
        return len(self.calcs) - 1, code

    def find_highest_sign(self, exp):
        # todo: reduce to just one for loop
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
        return

    def assign_blank(self, exp):
        code = str(randint(100000, 999999))
        code = "".join(chr(ord("A") + int(c)) for c in code)
        assert code not in self.calcs
        self.calcs[code] = Poly(exp, code)
        return code

    def replace_exp(self, exp):
        act_index = self.find_highest_sign(exp)
        if act_index == -5:
            return self.assign_blank(exp)
        left = act_index - 2
        while exp[left] != " " and left > 0:
            left -= 1
        right = act_index + 2
        while exp[right] != " " and right < len(exp) - 1:
            right += 1
        split_exp = exp[left:right + 1].split(" ")
        print(split_exp)
        split_exp = [c for c in split_exp if c not in [" ", ""]]
        try:
            a, act, b = split_exp
        except ValueError:
            print(exp)
            print(split_exp)
            exit()
        ref_index, code = self.get_calc(a, act, b)
        return exp[:left] + " " + code + exp[right:]

    def is_clean(self, eq):  # sourcery skip
        for char in eq:
            if char.isdigit():
                return False
            if char in self.actions:
                return False
        return True

    def convert_to_calc(self, eq):
        while not self.is_clean(eq):
            eq = self.replace_exp(eq)
        return eq

    def print_calcs(self):
        for key in self.calcs:
            print(str(self.calcs[key]) + f" of type {type(self.calcs[key])}")
        return

    def tidy(self, eq):
        left, right = eq.split("=")
        left, right = self.space(left), self.space(right)
        left, right = self.convert_to_calc(left), self.convert_to_calc(right)
        self.print_calcs()
        return left.strip(), right.strip()

    def compute(self, id):
        obj = self.calcs[id]
        return obj.compute()

    def solve_eq(self, eq):
        left, right = self.tidy(eq)
        left, right = self.compute(left), self.compute(right)
        print(left, "=", right)
        poly = left.merge(right)
        print(poly)
        return roots(poly)
