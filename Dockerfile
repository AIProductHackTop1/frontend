FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY fonts fonts
COPY app.py app.py
COPY utils.py utils.py

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
