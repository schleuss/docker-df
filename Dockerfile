FROM python:3.10-slim

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD docker-df.py /app

ENTRYPOINT ["/usr/local/bin/python", "/app/docker-df.py"]