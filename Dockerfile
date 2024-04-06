FROM python:3.11
LABEL authors="wen"

CMD pip install -r requirements.txt

ENTRYPOINT ["python", "-b"]