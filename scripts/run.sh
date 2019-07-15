#!/bin/bash

# runs provided service

if [ "x$1" == "x" ]
then
echo -e "\e[91mYou must provide a service\e[0m"
else
# count docker containers with name of passed name
COUNT=$(docker ps -a --no-trunc -f name=^/$1$ | wc -l)

# stop and remove containers with passed name
if [ "$COUNT" == "2" ]
then
echo "Container named $1 already exists, removing it..."
docker stop $1 >> /dev/null
docker rm $1 >> /dev/null
fi

# run service with passed name
echo -e "\e[1mRunning service: $1 as a daemon:\e[0m"
echo -e "- stop with \e[33m\`docker-compose stop $1\`\e[0m"
echo -e "- view logs with \e[33m\`docker-compose logs -f $1\`\e[0m"
echo -e "\e[1mdocker output:\e[0m"
docker-compose up -d $1
fi
