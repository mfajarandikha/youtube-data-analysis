FROM apache/airflow:2.8.1-python3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
