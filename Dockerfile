FROM python:3.11

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY fonts fonts
COPY app.py app.py
COPY utils.py utils.py

EXPOSE 8501
# Ссылка на бекенд
ENV BACKEND_URL="http://84.201.149.200:8000/"

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
