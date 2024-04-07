FROM python:3.11
LABEL authors="wen"

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV ENV_FILE_LOCATION=./.env

CMD ["python", "src/main.py"]