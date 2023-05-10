#!/bin/bash

REMOTE_IP=""

ping -c 1 $REMOTE_IP > /dev/null

if [ $? -ne 0 ]
then
    echo "remote server is down, running scripts locally."
    sh /home/$USER/twitter-kpi/check_scripts.sh
else
    echo "remote server is up."
fi
