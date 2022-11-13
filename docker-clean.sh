#!/bin/bash

# stop the containers:
docker-compose down
# delete all containers:
if [ $(docker ps -a -q) != "" ]; then
    docker rm -f $(docker ps -a -q)
fi
# delete all volumes:
if [ $(docker volume ls -q) != "" ]; then
    docker volume rm $(docker volume ls -q)
fi