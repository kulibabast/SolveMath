import sympy as sm
from GeneralFunctions import split_params


def C_n_k(n, k):
    n, k = int(split_params(n)), int(split_params(k))
    n_k = n - k
    number = sm.binomial(n, k)
    answer_format = "C({n}, {k}) = ({n}!) / ({k}! * {n_k}!) = {number}"
    return answer_format.format(n=n, k=k, number=number, n_k=n_k)


def A_n_k(n, k):
    n, k = int(split_params(n)), int(split_params(k))
    n_k = n - k
    i = n
    number = 1
    while i > n_k:
        number *= i
        i -= 1
    answer_format = "A({n}, {k}) = ({n}!) / ({n_k}!) = {number}"
    return answer_format.format(n=n, k=k, number=number, n_k=n_k)



func_dict = {
    'C': C_n_k,
    'A': A_n_k
}


def solve_combinatorics(func_name, request):
    return func_dict[func_name](*request.split(';'))