FROM python:3.10-alpine3.15

ENV PYTHONUNBUFFERED 1

COPY . /app

VOLUME ["/app"]

WORKDIR /app

EXPOSE 8000

RUN pip install -r requirements.txt



