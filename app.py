from utils import load_image, create_pdf

import os
import streamlit as st
import pandas as pd


def main():
    backend_url = os.getenv("BACKEND_URL")

    if backend_url is None:
        raise ValueError("BACKEND_URL environment variable is not set")

    # Заголовок приложения
    st.title("Автоматизированная система компьютерного зрения для поиска дефектов паллетов")

    # Создание вкладок
    tab1, tab2, tab3, tab4 = st.tabs(["Загрузка изображения", "Сформировать отчет", "История сессий", "О приложении"])

    # Вкладка 1: Загрузка изображения
    with tab1:
        st.header("Загрузите ваше изображение")
        img, classification_result = load_image(backend_url)

    # Вкладка 2: Сформировать отчет
    with tab2:
        st.header("Сформировать отчет")
        if img and "upload_history" in st.session_state and st.session_state.upload_history:
            file_info = st.session_state.upload_history[-1]
            pdf_file = create_pdf(image=img, file_info=file_info, classification_result=classification_result)
        
            # Кнопка для скачивания PDF с изображением и логами
            st.download_button(label="Скачать PDF", data=pdf_file, file_name="report.pdf", mime="application/pdf")
        else:
            st.write("Пожалуйста, сначала загрузите изображение на первой вкладке.")

    # Вкладка 3: История сессий
    with tab3:
        if "upload_history" in st.session_state:
            df = pd.DataFrame(st.session_state.upload_history)
            st.subheader("История сессий")
            st.dataframe(df)
        # Кнопка для очистки истории загрузок
        if st.button("Очистить историю"):
            st.session_state.upload_history = []
            st.write("История очищена.")

    # Вкладка 4: О приложении
    with tab4:
        st.header("О приложении")
        
        # Использование st.markdown для форматирования текста
        st.markdown("""
        <div style="text-align: justify;">
        Добро пожаловать в приложение для автоматизированного анализа изображений паллетов! Это веб-приложение использует технологии компьютерного зрения для выявления дефектов на паллетах. Вот как оно работает:

        1. **Загрузка изображения**: На первой вкладке вы можете загрузить изображение паллета. После загрузки изображения, система отображает его на экране и предлагает вам классифицировать его.

        2. **Создание отчета**: На второй вкладке можно сформировать отчет в формате PDF, который включает загруженное изображение и логгированную информацию о нем, такую как имя файла, размер, формат и время загрузки.

        3. **История сессий**: Третья вкладка предоставляет доступ к истории загруженных изображений и отчетов. Вы можете просмотреть все предыдущие загрузки и отчеты, а также очистить историю при необходимости.

        4. **О приложении**: В этой вкладке вы найдете информацию о функционале приложения и его возможностях.

        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

