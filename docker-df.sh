#!/bin/bash

DOCKER_SOCKET="/var/run/docker.sock"
DOCKER_DATA="/var/lib/docker"
IMAGE="schleuss/docker-df:latest"

if [ "$1" == "-h" ] || [ "$1" == "--help" ]
then
    echo "Usage: "
    echo "  "
    echo "  $0"
    echo "      - list of all containers"
    echo "  "    
    echo "  $0  <search> [-f|--full]"
    echo "      - Show information about the container with id = <search> or name = <search>"
    echo "      - If the [-f|--full] option is informed, include the size of shared volumes (with other containers)"
    echo "  "
else 
    docker run -it --rm --name tool-docker-df \
        -v "${DOCKER_SOCKET}:/var/run/docker.sock" \
        -v "${DOCKER_DATA}:${DOCKER_DATA}" $IMAGE $@
fi

