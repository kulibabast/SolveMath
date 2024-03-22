import sympy as sm
from sympy import symbols, sympify, diff, simplify, solve
from MathTools.GeneralFunctions import split_params, split_params_for_equation
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


def differentiate(pol: str, variable: str):
    pol = sympify(split_params(pol))
    variable = symbols(split_params(variable))
    f_prime = diff(pol, variable)
    return str(f_prime).replace("**", '^')


def solve_equation(equation: str, variable: str):
    equation_input, variable = split_params_for_equation(equation), split_params(variable)
    variable = symbols(variable)
    left_expression, right_expression = equation_input.split('=')
    left_side = sympify(left_expression)
    right_side = sympify(right_expression)
    equation = left_side - right_side
    solution = solve(equation, variable)
    set_solve = ';'.join(map(str, solution))
    return set_solve


func_dict = {
    'discriminant': calk_discriminant,
    'binomialTheorem': binomial_theorem,
    'vertexOfParabola': vertex_of_parabola,
    'solveLinearEquations': solve_linear_equations,
    'differentiate': differentiate,
    'solveEquation': solve_equation,
}


def solve_polynomial(func_name, request):
    return func_dict[func_name](*request.split(';'))
