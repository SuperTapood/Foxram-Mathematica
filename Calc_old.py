class Poly:
    def __init__(self, value, code):
        self.coeffs = {}
        coeff, power = self.get_info(value)
        self.coeffs[power] = coeff
        self.code = code
        return

    @staticmethod
    def get_info(exp):
        value = ""
        power = 0
        for char in exp:
            if not char.isdigit() and char != " ":
                # todo: identify higher powers and different variables
                power = 1
            elif char.isdigit() or char == "-":
                print(char)
                value += char
        if value == "":
            value = 1
        return int(value), power

    def __str__(self):
        return f"({self.code} - {self.coeffs})"

    def strip(self):
        return self

    def __add__(self, other):
        if type(other) == Poly:
            for key in other.coeffs:
                if key in self.coeffs:
                    self.coeffs[key] += other.coeffs[key]
                else:
                    self.coeffs[key] = other.coeffs[key]
        elif type(other) == Calc:
            return Add(self, other, None)
        else:
            coeff, power = self.get_info(other)
            print("info", other, coeff, power)
            if power not in self.coeffs:
                self.coeffs[power] = coeff
            else:
                self.coeffs[power] += coeff
        return self

    def __sub__(self, other):
        coeff, power = self.get_info(other)
        if power not in self.coeffs:
            self.coeffs[power] = -coeff
        elif type(other) == Calc:
            return Sub(self, other)
        else:
            self.coeffs[power] -= coeff
        return self

    def __mul__(self, other):
        # todo: count the power in
        if type(other) == Poly:
            for key in other.coeffs:
                if key in self.coeffs:
                    self.coeffs[key] *= other.coeffs[key]
        elif type(other) == Calc:
            return Mult(self, other)
        else:
            coeff, power = self.get_info(other)
            for key in self.coeffs:
                self.coeffs[key] *= coeff
        return self

    # todo: __div__

    def compute(self):
        return self

    def merge(self, other):
        for key in other.coeffs:
            if key not in self.coeffs:
                self.coeffs[key] = -other.coeffs[key]
            else:
                self.coeffs[key] -= other.coeffs[key]
        highest_power = max(self.coeffs.keys())
        roots = [0] * (highest_power + 1)
        for key in self.coeffs:
            roots[key] = self.coeffs[key]
        return roots


class Calc:
    def __init__(self, a, b, code):
        self.a = a
        if type(a) == str:
            for char in a:
                if not char.isdigit():
                    self.a = Poly(a, None)
        self.b = b
        if type(b) == str:
            for char in b:
                if not char.isdigit():
                    self.b = Poly(b, None)
        self.code = code
        return

    def prep(self):
        if type(self.a) == Calc:
            self.a = self.a.compute()
        if type(self.b) == Calc:
            self.b = self.b.compute()
        return

    def __str__(self):
        return f"{self.code} -> {self.a} {self.type} {self.b}"

    pass


class Add(Calc):
    type = "+"

    def compute(self):
        self.prep()
        return self.a + self.b

    pass


class Sub(Calc):
    type = "-"

    def compute(self):
        self.prep()
        return self.a - self.b

    pass


class Mult(Calc):
    type = "*"

    def compute(self):
        self.prep()
        return self.a * self.b

    pass


class Div(Calc):
    type = "/"

    def compute(self):
        self.prep()
        return self.a / self.b

    pass
