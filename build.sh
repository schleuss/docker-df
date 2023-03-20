#!/bin/bash

docker build . --tag schleuss/docker-df:latest
docker push schleuss/docker-df:latest
