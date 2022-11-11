#!/bin/bash

# stop the containers:
docker-compose down
# delete all containers:
docker rm -f $(docker ps -a -q)
# delete all volumes:
docker volume rm $(docker volume ls -q)