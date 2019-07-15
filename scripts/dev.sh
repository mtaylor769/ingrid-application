#!/bin/bash

# runs provided service container with bash shell
if [ "x$1" == "x" ]
then
echo -e "\e[91mYou must provide a service\e[0m"
else
# count docker containers with name of passed name
COUNT=$(docker ps -a --no-trunc -f name=^/$1$ | wc -l)

# stop and remove containers with passed name
if [ "$COUNT" == "2" ]
then
echo "Container '$1' already exists, removing it..."
docker stop $1 >> /dev/null
docker rm $1 >> /dev/null
fi

# run service with passed name and override command
docker-compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml run --service-ports --name $1 $1 /bin/bash
fi

