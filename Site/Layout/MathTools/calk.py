from MathTools.GeneralFunctions import split_params
import sympy as sm
from math import gcd, ceil
import random


def fact(n):
    n = int(split_params(n))
    answer_format = f"{n}! = {sm.factorial(n)}"
    return answer_format.format()


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


def brent_factorization(n):
    if n % 2 == 0:
        return [2] + brent_factorization(n // 2)

    if is_prime(n):
        return [n]

    y, c, m = random.randint(1, n - 1), random.randint(1, n - 1), random.randint(1, n - 1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (y * y + c) % n
        k = 0
        while k < r and g == 1:
            ys = y
            for i in range(min(m, r - k)):
                y = (y * y + c) % n
                q = q * (abs(x - y)) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (ys * ys + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break

    if is_prime(g):
        return [g] + brent_factorization(n // g)
    else:
        return brent_factorization(g) + brent_factorization(n // g)


def prime_factorization(n: str):
    n = int(split_params(n))
    factors = {}
    for factor in brent_factorization(n):
        factors[factor] = factors.get(factor, 0) + 1
    answer = ''
    for key in factors:
        answer += f'{key}^{factors[key]} * '
    return answer[:-3]


def check_mod(n, m):
    n, m = int(split_params(n)), int(split_params(m))
    if n % m == 0:
        return f'{n} делится нацело на {m} ({n} / {m} = {n // m})'
    return f'{n} не делится нацело на {m} ({n} по модулю {m} = {n % m})'


def get_mod(n, m):
    n, m = int(split_params(n)), int(split_params(m))
    return f'{n} по модулю {m} = {n % m}'


def round_number(n, comands):
    n, comands = float(split_params(n)), split_params(comands)
    if comands == 'up':
        return str(ceil(n))
    elif comands == 'down':
        return str(int(n))
    else:
        return str(round(n, int(comands)))


func_dict = {
    'fact': fact,
    'pow': fast_pow,
    'evalWithNumber': eval_quotient_with_number,
    'primefactorsNumber': prime_factorization,
    'checkMod': check_mod,
    'getMod': get_mod,
    'roundNumber': round_number
}


def solve_calk(func_name, request):
    return func_dict[func_name](*request.split(';'))