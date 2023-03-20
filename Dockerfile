FROM python:3.10-slim

RUN pip3 install docker

WORKDIR /app

ADD docker-df.py /app

ENTRYPOINT ["/usr/local/bin/python", "/app/docker-df.py"]