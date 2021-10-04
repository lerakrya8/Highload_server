FROM python:3.8

WORKDIR /app

ADD . /app

EXPOSE 81

CMD ["python3", "main.py"]