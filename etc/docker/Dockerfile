FROM python:3.6-slim

ENV PYTHONUNBUFFERED=0

RUN apt-get update && apt-get install git -y

WORKDIR /opt/is-commtrace-exporter

COPY . .

RUN pip install .

RUN pip install -I "git+https://github.com/labviros/opencensus-python.git"