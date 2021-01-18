from numpy import zeros, roots


class Info:
    dic = {}
    pass


class Poly:
    def __init__(self, value, code):
        self.coefficients = {}
        try:
            value = float(value)
        except ValueError as e:
            try:
                value = Info.dic[value].compute()
            except KeyError:
                power, coefficient = self.extract(value)
                self.coefficients[power] = coefficient
        if type(value) == Poly:
            self.copy(value)
        else:
            power, coefficient = self.extract(value)
            self.coefficients[power] = coefficient
        return

    def compute(self):
        return self

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
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] *= other.coefficients[key]
        return self

    def __truediv__(self, other):
        assert type(other) == Poly
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] /= other.coefficients[key]
        return self

    def strip(self):
        return self

    @staticmethod
    def extract(value):
        power = 0
        coefficient = ""
        for char in str(value):
            if char.isdigit() or char == "." or char == "-":
                coefficient += char
            elif char not in [" ", ""]:
                # todo: add compatibility for higher powers
                power = 1
        try:
            float(coefficient)
        except ValueError:
            if power == 1:
                coefficient = 1
            else:
                raise Exception("AAAAAAAAA")
        return power, float(coefficient)

    def merge(self, other):
        assert type(other) == Poly
        for key in other.coefficients:
            if key in self.coefficients:
                self.coefficients[key] -= other.coefficients[key]
            else:
                self.coefficients[key] = -other.coefficients[key]
        return self

    def solve(self):
        if len(self.coefficients) == 1:
            return self.coefficients[0]
        poly = zeros(shape=max(self.coefficients) + 1)
        for key in self.coefficients:
            poly[key] = self.coefficients[key]
        print(poly)
        exit()
        return roots(poly)

    def copy(self, other):
        for key in other.coefficients:
            self.coefficients[key] = other.coefficients[key]
        return

    pass
