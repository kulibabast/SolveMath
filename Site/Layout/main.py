import streamlit as st
import pandas as pd
from MathTools.main import solve
from MathTools.polynomial import kramer_method
import re
import sympy as sm
from MlService.main import generate_response, get_predictions_theory, \
                            get_predictions_topic
import plotly.graph_objs as go



NAME_TOPIC = ['Геометрия', 'Дирихле',
              'Инвариант', 'Многочлен',
              'Комбинаторика', 'Оценка+Пример',
              'Теория чисел', 'Графы']


def gen_solve():
    st.title("Генерация решения")
    messages = st.container()
    if prompt := st.chat_input("Введите условие..."):
        messages = st.container()
        messages.chat_message("user", avatar="👽").write(prompt)
        messages.chat_message("bot", avatar="🤖").write(f"Получил! В процессе решения...")
        answer = generate_response(prompt)
        messages.chat_message("bot", avatar="🤖").write(answer)


def topic_class():
    st.title("Классификация темы")
    user_input = st.text_input("Введите условие:")
    ver = st.number_input('Введите минимальную вероятность уверенности',
                          min_value=0, max_value=99, step=1)

    if st.button("Нажмите для обработки", type="primary"):
        if user_input:
            answer, prob = get_predictions_topic(user_input)
            st.markdown(f"### Наиболее вероятные темы:")
            for name in answer:
                if int(answer[name]) <= ver:
                    break
                st.write(f'{name} - {answer[name]}%')

            fig = go.Figure(data=[go.Pie(labels=NAME_TOPIC, values=prob)])
            fig.update_layout(width=800, height=600,
                              margin=dict(
                                  l=0.5,  # Отступ слева
                                  r=0,  # Отступ справа
                                  t=0,  # Отступ сверху
                                  b=0.3,  # Отступ снизу
                              ),
                              legend=dict(orientation="h",
                                          xanchor="center",
                                          yanchor="top",
                                          x=0.4,
                                          y=-0.3,
                                          font=dict(size=18, )
                                          ))
            st.plotly_chart(fig)
        else:
            st.error("Пожалуйста, введите условие ")


def prediction_theory():
    st.title("Предположение теории")
    user_input = st.text_input("Введите условие:")
    ver = st.number_input('Введите минимальную вероятность уверенности',
                          min_value=0, max_value=99, step=1)
    if st.button("Нажмите для обработки", type="primary"):
        if user_input:
            answer = get_predictions_theory(user_input)
            st.markdown(f"### Наиболее вероятные темы:")
            for name in answer:
                if int(answer[name]) <= ver:
                    break
                st.write(f'{name} - {answer[name]}%')
        else:
            st.error("Пожалуйста, введите условие")


def math_tools():
    st.title("Математические инструменты")
    option = st.selectbox(
        'Выберите вариант',
        ('Формула сочетаний', 'Формула размещений',
         'Бином Ньютона', 'Решение линейных уравнений',
         "Подсчет дискриминанта", "Узнать координаты вершины",
         "Вычисление производной", 'Факторизация числа',
         "Вычислить выражение", "Вычислить делители числа",
         "Решить уравнение")
    )

    if option == 'Формула сочетаний':
        n = st.number_input('Введите n', min_value=0, step=1)
        k = st.number_input('Введите k', min_value=0, step=1)
        if st.button("Рассчитать", type="primary"):
            if n and k:
                answer = solve(f'combinatorics_C_n={n};k={k}')
                answer = list(map(lambda x: x.replace(' ', ""), re.split(r'[=/]', answer)))
                answer = answer[0] + ' = ' + '\dfrac{' + answer[1][1:-1] + '}' \
                        '{' + answer[2][1:-1] + '}' + f' = {answer[3]}'
                print(answer)
                st.markdown("### Решение:")
                st.latex(answer)
            else:
                st.error("Пожалуйста, введите параметры")
    elif option == 'Формула размещений':
        n = st.number_input('Введите n', min_value=0, step=1)
        k = st.number_input('Введите k', min_value=0, step=1)
        if st.button("Рассчитать", type="primary"):
            if n and k:
                answer = solve(f'combinatorics_A_n={n};k={k}')
                answer = list(map(lambda x: x.replace(' ', ""), re.split(r'[=/]', answer)))
                answer = answer[0] + ' = ' + '\dfrac{' + answer[1][1:-1] + "}" \
                                    "{" + answer[2][1:-1] + '}' + f' = {answer[3]}'
                st.markdown("### Решение:")
                st.latex(answer)
            else:
                st.error("Пожалуйста, введите параметры")
    elif option == 'Бином Ньютона':
        a = st.number_input('Введите a', min_value=0, step=1)
        b = st.number_input('Введите b', min_value=0, step=1)
        n = st.number_input('Введите n', min_value=0, step=1)
        if st.button("Рассчитать", type="primary"):
            if n and b and n:
                answer = solve(f'polynomial_binomialTheorem_equation=({a}+{b})^{n}')
                st.markdown("### Решение:")
                st.latex(answer)
            else:
                st.error("Пожалуйста, введите параметры")

    elif option == 'Решение линейных уравнений':
        n = st.number_input('Введите количество переменных', min_value=0, max_value=9, step=1)
        if n:
            df = pd.DataFrame([{f'k_{num}': 0 for num in range(1, n+1)} for _ in range(n)])
            df['y'] = 0
            edited_df = st.data_editor(df)
            if st.button("Рассчитать", type="primary"):
                X = edited_df[[column for column in edited_df.columns if column != 'y']].values
                Y = edited_df['y'].values
                answer = kramer_method(sm.Matrix(X), sm.Matrix(Y))
                st.markdown("### Решение:")
                st.write(answer.replace('\n', '\n\n'))
    elif option == 'Подсчет дискриминанта':
        df = pd.DataFrame([{'a': 1, "b": 0, 'c': 0}])
        edited_df = st.data_editor(df)
        if st.button("Рассчитать", type="primary"):
            a, b, c = edited_df['a'][0], edited_df['b'][0], edited_df['c'][0]
            if a != 0:
                answer = solve(f'polynomial_discriminant_equation={a}*x^2+({b})*x+({c});variable=x')
                st.markdown("### Решение:")
                st.latex(answer)
            else:
                st.error('очень вкусно и точка')
    elif option == 'Узнать координаты вершины':
        df = pd.DataFrame([{'a': 0, "b": 0, 'c': 0}])
        edited_df = st.data_editor(df)
        if st.button("Рассчитать", type="primary"):
            a, b, c = edited_df['a'][0], edited_df['b'][0], edited_df['c'][0]
            if a != 0:
                equation = f'{a}*x^2+({b})*x+({c})'
                answer_x, answer_y = solve(f'polynomial_vertexOfParabola_equation={equation};variable=x')
                st.markdown("### Решение:")
                st.latex(equation)
                st.latex(answer_x)
                st.latex(answer_y)
            else:
                st.error('очень вкусно и нет точки')
    elif option == "Вычисление производной":
        pol = st.text_input("Введите уравнение:")
        variable = st.text_input("По какой переменной продифференцировать:")
        st.write("Ваше уравнение выглядит так: ")
        st.latex(pol)
        st.write("Переменная: ")
        st.latex(variable)

        if st.button("Рассчитать", type="primary"):
            answer = solve(f'polynomial_differentiate_pol={pol};variable={variable}')
            print(answer)
            st.markdown("### Решение:")
            answer = '\dfrac{' + pol + '}' + '{d' + variable + '}' " = " + answer
            st.latex(answer)
    elif option == "Вычислить выражение":
        quotient = st.text_input("Введите выражение:")
        st.write("Ваше уравнение выглядит так: ")
        st.latex(quotient)

        if st.button("Рассчитать", type="primary"):
            answer = solve(f'calk_evalWithNumber_quotient={quotient}')
            st.markdown("### Ответ:")
            st.latex(answer)
    elif option == "Факторизация числа":
        n = st.number_input('Введите число', min_value=1, step=1)
        if st.button("Рассчитать", type="primary"):
            answer = solve(f'calk_primefactorsNumber_n={n}')
            st.latex(f'{n} = ' + answer)
    elif option == "Вычислить делители числа":
        n = st.number_input('Введите число', min_value=1, step=1)
        if st.button("Рассчитать", type="primary"):
            answer = solve(f'calk_findDivisors_n={n}')
            st.write(answer)
    elif option == "Решить уравнение":
        equation = st.text_input("Введите уравнение:")
        variable = st.text_input("По какой переменной решить:")
        st.write("Ваше уравнение выглядит так: ")
        st.latex(equation)
        st.write("Переменная: ")
        st.latex(variable)

        if st.button("Рассчитать", type="primary"):
            answer = solve(f'polynomial_solveEquation_equation={equation};variable={variable}')
            answer = answer.split(';')
            st.markdown("### Уравнение имеет следующие корни:")
            for ind, value in enumerate(answer):
                st.latex(value)



def main():
    st.sidebar.title("Разделы")
    selected_section = st.sidebar.radio(
        "Перейти к разделу:",
        ("Генерация решения",
         "Классификация темы",
         "Предположение теории",
         "Математические инструменты")
    )

    if selected_section == "Генерация решения":
        gen_solve()
    elif selected_section == "Классификация темы":
        topic_class()
    elif selected_section == "Предположение теории":
        prediction_theory()
    elif selected_section == "Математические инструменты":
        math_tools()


if __name__ == "__main__":
    main()