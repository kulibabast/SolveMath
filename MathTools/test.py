from sympy import sympify, solve, symbols

# Ввод уравнения с консоли
equation_input = input("Введите уравнение (без пробелов вокруг знака '='): ")
variable = input('Значение переменной: ')
variable = symbols(variable)
left_expression, right_expression = equation_input.split('=')
left_side = sympify(left_expression)
right_side = sympify(right_expression)
equation = left_side - right_side
solution = solve(equation, variable)
print(f"Решение уравнения: {equation} {solution}")