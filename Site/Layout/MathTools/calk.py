from MathTools.GeneralFunctions import split_params
import sympy as sm
from math import gcd, ceil
import random
import math


def fast_pow(x, y):
    x, y = int(split_params(x)), int(split_params(y))
    s, v, c = 1, y, x
    while v > 0:
        if v % 2 == 1:
            s = s * c
        v = v >> 1
        c = c * c
    return f'{x}^{y} = {s}'


def eval_quotient_with_number(quotient: str):
    quotient = split_params(quotient)
    x = sm.symbols('x')
    new_quotient = sm.sympify('x+' + quotient)
    result = new_quotient.subs(x, 0)
    answer_format = f'{quotient} = {result}'
    return answer_format


def is_prime(x):
    if x <= 1:
        return False
    if x == 2 or x == 3:
        return True
    if x % 2 == 0:
        return False
    i = 5
    while i * i <= x:
        if x % i == 0 or x % (i + 2) == 0:
            return False
        i += 6
    return True


def factorize_number(n):
    n = int(split_params(n))
    factors = []
    divisor = 2

    while n > 1:
        if n % divisor == 0:
            count = 0
            while n % divisor == 0:
                n //= divisor
                count += 1
            factors.append((divisor, count))
        divisor += 1

    return format_factors(factors)


def format_factors(factors):
    formatted_factors = []
    for factor, count in factors:
        formatted_factors.append(f"{factor}^{count}")
    return " * ".join(formatted_factors)


def find_divisors(n):
    n = int(split_params(n))
    divisors = []
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    divisors = list(map(str, sorted(divisors)))
    return f'Число {n} имеет делители: {", ".join(divisors)}'


func_dict = {
    'evalWithNumber': eval_quotient_with_number,
    'primefactorsNumber': factorize_number,
    'findDivisors': find_divisors,
}


def solve_calk(func_name, request):
    return func_dict[func_name](*request.split(';'))