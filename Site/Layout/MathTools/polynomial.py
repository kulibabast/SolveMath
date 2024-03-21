import sympy as sm
from sympy import symbols, sympify, expand, diff, factor, trigsimp, simplify
from sympy.polys.polytools import div
from MathTools.GeneralFunctions import split_params
from MathTools.calk import fast_pow
import re


def get_params(equation: str, variable: str):
    equation = split_params(equation)
    x = symbols(split_params(variable))
    poly_expression = sm.Poly(equation, x)
    return poly_expression.all_coeffs()


def calk_discriminant(equation: str, variable: str):
    a, b, c = get_params(equation, variable)
    discriminant = simplify(f'{b} * {b} - 4 * {a} * {c}')
    answer = "D = {b}^2 - 4{a}*{c} = {discriminant}"
    return answer.format(a=a, b=b, c=c, discriminant=discriminant)


def binomial_theorem(equation: str):
    equation = split_params(equation)
    a, b, n = map(int, equation.replace('(', "")\
                      .replace('+', " ")\
                      .replace(')^', " ")\
                      .split()
                  )
    equation_answer = f"C({n}, {0}) * {a}^{n-0} * {b}^{0}"
    for k in range(1, n+1):
        equation_answer += f' + C({n}, {k}) * {a}^{n-k} * {b}^{k}'
    answer = f'{equation} = {equation_answer} = {fast_pow(f"x={a + b}", f"n={n}").split(" = ")[1]}'
    return answer


def vertex_of_parabola(equation: str, variable: str):
    a, b, c = get_params(equation, variable)
    x = simplify(f'- ({b}) / (2 * ({a}))')
    y = simplify(f'{c} - ({b})^2 / (4 * ({a}))')
    a, b, c, x, y = map(str, [a, b, c, x, y])
    answer_x = "x = - \dfrac{(" + b + ")}{(2 * (" + a + "))}" + f" = {x}"
    answer_y = f"y = {c} - " + "\dfrac{(" + f"{b}^2)" + "}{(4 * " + a + ")}" + f" = {y}"
    return answer_x, answer_y


def kramer_method(coefficients_matrix, constants_vector):
    result = ''
    num_equations = len(constants_vector)
    determinant_main = coefficients_matrix.det()
    solutions = []

    if determinant_main == 0:
        return "Система уравнений вырожденная, решений нет"
    result += f"Определитель основной матрицы коэффициентов: {determinant_main}\n"

    for i in range(num_equations):
        matrix_copy = coefficients_matrix.copy()
        matrix_copy[:, i] = constants_vector
        determinant_sub = matrix_copy.det()
        solution = str(determinant_sub / determinant_main).rstrip('.0')
        result += f"Определитель матрицы после замены столбца {i+1} на вектор правой части: {determinant_sub}\n"
        result += f"Решение для переменной {i+1}: {determinant_sub} / {determinant_main} = {solution}\n"
        solutions.append(solution)
    result += 'Ответ: ('
    for i in solutions:
        result += f'{i}, '
    result = result[:-2] + ')'
    return result


def processing_equation(elem):
    for ind, chars in enumerate(elem):
        if chars.isalpha() and chars not in ('+', '-', '.'):
            return int(elem[:ind])


def solve_linear_equations(equation: str):
    equation = split_params(equation)
    coefficients_matrix = []
    constants_vector = []
    for eq in equation.split('|'):
        *right, left = re.findall(r'[-+]?\d+[a-zA-Z]*', eq)
        coefficients_matrix.append(list(map(processing_equation, right)))
        constants_vector.append(int(left))
    result = kramer_method(sm.Matrix(coefficients_matrix), sm.Matrix(constants_vector))
    return result


def transformation_polynomials(pol1: str, pol2: str, action: str):
    pol1, pol2, action = split_params(pol1), split_params(pol2), \
                                split_params(action)
    pol_1 = sympify(pol1)
    pol_2 = sympify(pol2)

    if action == 'div':
        quotient, remainder = div(pol_1, pol_2)
        answer_format = f'{pol_1} / {pol_2}:\nчастное: {quotient}\nостаток: {remainder}'
    elif action == 'sum':
        result = pol_1 + pol_2
        answer_format = f'{pol_1} + {pol_2} = {result}'
    elif action == 'dif':
        result = pol_1 - pol_2
        answer_format = f'{pol_1} - {pol_2} = {result}'
    elif action == 'expand':
        result = expand(pol_1 * pol_2)
        answer_format = f'{pol_1} * {pol_2} = {result}'
    else:
        raise ValueError(f'{action} not found')
    return answer_format.replace("**", '^')


def differentiate(pol: str, variable: str):
    pol = sympify(split_params(pol))
    variable = symbols(split_params(variable))
    f_prime = diff(pol, variable)
    answer_format = f'Производная {pol} по переменной {variable} = {f_prime}'
    return answer_format.replace("**", '^')


def simplify_polynomial(pol: str):
    return str(sympify(split_params(pol))).replace("**", '^')


def factor_polynomial(pol: str):
    return str(factor(split_params(pol))).replace("**", '^')


def solve_trigonometric(pol: str):
    return str(trigsimp(split_params(pol))).replace("**", '^')



func_dict = {
    'discriminant': calk_discriminant,
    'binomialTheorem': binomial_theorem,
    'vertexOfParabola': vertex_of_parabola,
    'solveLinearEquations': solve_linear_equations,
    'transformationPolynomials': transformation_polynomials,
    'differentiate': differentiate,
    'simplifyPolynomial': simplify_polynomial,
    'factorPolynomial': factor_polynomial,
    'solveTrigonometric': solve_trigonometric
}


def solve_polynomial(func_name, request):
    return func_dict[func_name](*request.split(';'))
