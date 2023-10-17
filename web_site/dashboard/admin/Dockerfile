FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
COPY datasets/ ./datasets/
COPY src/ ./src/
COPY app.py ./app.py

# RUN apt-get update && \
#     apt-get install -y awscli

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
