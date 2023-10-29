FROM python:3.9-slim

WORKDIR /code

RUN apt-get update
RUN apt-get install libeccodes0 -y
RUN apt-get install awscli -y

COPY . .

RUN ["pip", "install", "-r", "requirements.txt"]

ENTRYPOINT ["python", "main.py"]
