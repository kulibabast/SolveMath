from math import gcd
import random


def brent_factorization(n):
    if n % 2 == 0:
        return [2] + brent_factorization(n // 2)

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


def prime_factorization(n):
    factors = {}
    for factor in brent_factorization(n):
        factors[factor] = factors.get(factor, 0) + 1
    return factors


# Пример использования
number = 20
result = prime_factorization(number)
print("Простые множители числа", number, ":", result)