import streamlit as st
from time import sleep
from MathTools.main import solve


def gen_solve():
    st.title("Генерация решения")
    messages = st.container()
    if prompt := st.chat_input("Введите условие..."):
        messages = st.container()
        messages.chat_message("user", avatar="👽").write(prompt)
        messages.chat_message("bot", avatar="🤖").write(f"Получил! В процессе решения...")
        sleep(0.5)
        messages.chat_message("bot", avatar="🤖").write(f"Готово!")


def topic_class():
    st.title("Классификация темы")
    user_input = st.text_input("Введите условие:")

    if st.button("Нажмите для обработки", type="primary"):
        if user_input:
            st.write("Это дирихле")
        else:
            st.error("Пожалуйста, введите условие")


def prediction_theory():
    st.title("Предположение теории")
    user_input = st.text_input("Введите условие:")

    if st.button("Нажмите для обработки", type="primary"):
        if user_input:
            st.write("Возможно, это Оценка+Пример")
        else:
            st.error("Пожалуйста, введите условие")


def math_tools():
    st.title("Математические инструменты")
    option = st.selectbox(
        'Выберите вариант',
        ('Формула сочетаний', 'Бином Ньютона', 'Решение линейных уравнений')
    )

    if option == 'Формула сочетаний':
        n = st.number_input('Введите n', min_value=0, step=1)
        k = st.number_input('Введите k', min_value=0, step=1)
        if st.button("Рассчитать", type="primary"):
            if n and k:
                answer = solve(f'combinatorics_C_n={n};k={k}')
                st.write(answer)
            else:
                st.error("Пожалуйста, введите параметры")
    elif option == 'Бином Ньютона':
        a = st.number_input('Введите a', min_value=0, step=1)
        b = st.number_input('Введите b', min_value=0, step=1)
        n = st.number_input('Введите n', min_value=0, step=1)
        if st.button("Рассчитать", type="primary"):
            if n and b and n:
                answer = solve(f'polynomial_binomialTheorem_equation=({a}+{b})^{n}')
                st.write(answer)
            else:
                st.error("Пожалуйста, введите параметры")

    elif option == 'Решение линейных уравнений':
        a = st.number_input('Введите a', min_value=0, step=1)
        b = st.number_input('Введите b', min_value=0, step=1)
        n = st.number_input('Введите n', min_value=0, step=1)
        if st.button("Рассчитать", type="primary"):
            if n and b and n:
                answer = solve(f'polynomial_binomialTheorem_equation=({a}+{b})^{n}')
                st.write(answer)
            else:
                st.error("Пожалуйста, введите параметры")

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