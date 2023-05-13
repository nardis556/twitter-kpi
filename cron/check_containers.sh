#!/bin/bash

sleep 10

CONTAINER_NAMES=("mysqlc" "phpc")

for CONTAINER_NAME in "${CONTAINER_NAMES[@]}"
do
    if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER_NAME)" != "true" ]; then
        echo "Docker container '$CONTAINER_NAME' has stopped."
        echo "Restarting '$CONTAINER_NAME'..."
        docker start $CONTAINER_NAME
    else
        echo "Docker container '$CONTAINER_NAME' is running."
    fi
done
