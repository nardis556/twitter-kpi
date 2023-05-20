#!/bin/bash

# check python scripts:
sleep 60

if pgrep -f "update_summaries.py" > /dev/null
then
    echo "update_summaries.py is running."
else
    echo "update_summaries.py is not running. Starting update_summaries.py"
    /home/lars/.pyenv/shims/python /home/lars/twitter-kpi/scripts/update_summaries.py &
fi

sleep 60

if pgrep -f "author_engagements.py" > /dev/null
then
    echo "author_engagements.py is running."
else
    echo "author_engagements.py is not running. Starting author_engagements.py"
    /home/lars/.pyenv/shims/python /home/lars/twitter-kpi/scripts/author_engagements.py &
fi

sleep 60

if pgrep -f "user_engagements.py" > /dev/null
then
    echo "user_engagements.py is running."
else
    echo "user_engagements.py is not running. Starting user_engagements.py"
    /home/lars/.pyenv/shims/python /home/lars/twitter-kpi/scripts/user_engagements.py &
fi

sleep 60

if pgrep -f "author_stats.py" > /dev/null
then
    echo "author_stats.py is running."
else
    echo "author_stats.py is not running. Starting author_stats.py"
    /home/lars/.pyenv/shims/python /home/lars/twitter-kpi/scripts/author_stats.py &
fi
