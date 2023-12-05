FROM python:3.10-slim

WORKDIR /app

COPY train.py df_test.parquet requirements.txt ./


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt