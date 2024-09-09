import os
import requests
import streamlit as st

from PIL import Image
from io import BytesIO
from datetime import datetime
from fpdf import FPDF



# Функция для загрузки изображения
def load_image():
    uploaded_file = st.file_uploader("Перетащите сюда изображение", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)
        result = st.button('Классифицировать изображение')
        
        if result:
            st.success('Success')
            file_info = {
						    "Имя файла": uploaded_file.name,
						    "Размер (KB)": len(image_data) / 1024.0,  
						    "Формат": Image.open(BytesIO(image_data)).format,
						    "Время загрузки": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						}
            
            st.write("Отправка запроса...")

            # Отправка POST-запроса к FastAPI
            url = "http://localhost:8000/api/classify"
            files = {"image": (uploaded_file.name, uploaded_file, uploaded_file.type)} 
            
            try:
                response = requests.post(url, files=files)
                st.write(f"Код ответа: {response.status_code}")
                
                if response.status_code == 200:
                    classification_result = response.json()
                    st.write(classification_result)
                else:
                    st.error(f"Ошибка при классификации изображения. Код ответа: {response.status_code}")
            
            except Exception as e:
                st.error(f"Ошибка при отправке запроса: {e}")

            if "upload_history" not in st.session_state:
                st.session_state.upload_history = []
            st.session_state.upload_history.append(file_info)

        return Image.open(BytesIO(image_data))
    else:
        st.write("Пожалуйста, загрузите изображение")
        return None

# Функция для создания PDF-файла
def create_pdf(image=None, file_info=None):
    pdf = FPDF()
    pdf.add_page()
    
    # Добавление шрифта, поддерживающего Unicode
    pdf.add_font('DejaVu', '', 'fonts/dejavu/DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', size=12)
    
    # Добавление текста
    pdf.cell(200, 10, txt="Отчет с изображением", ln=True, align='C')
    
    if image:
        # Сохранение изображения во временный файл
        temp_image_path = "temp_image.png"
        image.save(temp_image_path, format="PNG")
        
        # Добавление изображения в PDF
        pdf.image(temp_image_path, x=10, y=30, w=100)
        
        # Удаление временного файла после использования
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
    
    if file_info:
        pdf.ln(100)
        pdf.cell(200, 10, txt="Логгирование информации о загруженном изображении:", ln=True)
        pdf.cell(200, 10, txt=f"Имя файла: {file_info['Имя файла']}", ln=True)
        # Проверка типа данных перед форматированием
        size_kb = file_info['Размер (KB)']
        if isinstance(size_kb, (int, float)):
            pdf.cell(200, 10, txt=f"Размер (KB): {size_kb:.2f}", ln=True)
        else:
            pdf.cell(200, 10, txt=f"Размер (KB): {size_kb}", ln=True)
        pdf.cell(200, 10, txt=f"Формат: {file_info['Формат']}", ln=True)
        pdf.cell(200, 10, txt=f"Время загрузки: {file_info['Время загрузки']}", ln=True)

    pdf_output = pdf.output(dest='S').encode('latin1')  # Конвертация в байты с нужной кодировкой
    
    return BytesIO(pdf_output)