from random import randint

from poly import *

acts = {}
actions = ["-", "+", "/", "*"]


def print_sides(desc, left, right):
    print(desc, left + " = " + right)
    return


def dense(exp):
    return "".join(char for char in exp if char != " ")


def space(exp):
    out = " "
    current = ""
    for i, char in enumerate(exp):
        if char == "-":
            if i == 0 or exp[i - 1] in actions:
                current += char
            else:
                out += current + " " + char + " "
                current = ""
        elif char not in actions:
            current += char
        else:
            out += current + " " + char + " "
            current = ""
    out += current + " "
    return out


def not_clean(exp):  # sourcery skip
    for char in exp:
        if char.isdigit():
            return True
        if char in actions:
            return True
    return False


def find_index(exp):
    target = None
    for act in actions:
        if act in exp:
            target = act
            break
    if target is None:
        return -5
    for i, char in enumerate(exp):
        if char == target:
            return i


def generate_operation(a, act, b):
    num = randint(10000, 99999)
    code = "".join(chr(ord("A") + int(n)) for n in str(num))
    while code in acts:
        num = randint(10000, 99999)
        code = "".join(chr(ord("A") + int(n)) for n in str(num))
    if act == "+":
        acts[code] = Poly(a, code) + Poly(b, None)
    elif act == "-":
        acts[code] = Poly(a, code) - Poly(b, None)
    elif act == "*":
        acts[code] = Poly(a, code) * Poly(b, None)
    elif act == "/":
        acts[code] = Poly(a, code) / Poly(b, None)
    else:
        raise Exception("Action not found!")
    Info.dic = acts
    return code


def clean(exp):
    index = find_index(exp)
    left = index - 2
    while exp[left - 1] != " " and left > 0:
        left -= 1
    right = index + 2
    while exp[right + 1] != " " and right < len(exp) - 1:
        right += 1
    extracted = exp[left:right + 1].strip()
    splitted_extracted = extracted.split(" ")
    # this shit may raise an exception later about not having enough values
    # to unpack, do remember to check that it has enough spacing and that the
    # spacing algorithm does in fact work
    try:
        a, act, b = splitted_extracted
    except ValueError as e:
        print("Split is fucked again")
        print(exp)
        print(extracted)
        print(splitted_extracted)
        exit()
    code = generate_operation(a, act, b)
    exp = exp[:left] + code + exp[right + 1:]
    return exp


def get_calc(exp):
    if exp.strip().isnumeric():
        return Poly(exp, None)
    while not_clean(exp):
        exp = clean(exp)
        if not not_clean(exp):
            return exp
    return


def get_sides(left, right):
    if type(left) != Poly:
        left = acts[left]
    if type(right) != Poly:
        right = acts[right]
    return left, right


def to_poly(eq):
    global acts
    left, right = eq.split("=") if "=" in eq else (eq, "0")
    dense_left, dense_right = dense(left), dense(right)
    spaced_left, spaced_right = space(dense_left), space(dense_right)
    calc_left, calc_right = get_calc(spaced_left).strip(), get_calc(spaced_right).strip()
    # print_sides("basic", left, right)
    # print_sides("spaced", spaced_left, spaced_right)
    # print_sides("as object", calc_left, calc_right)
    return get_sides(calc_left, calc_right)
