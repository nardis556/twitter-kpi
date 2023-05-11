#!/bin/bash

if pgrep -f "build_followers.py" > /dev/null
then
    echo "build_followers.py is running."
else
    echo "build_followers.py is not running. Starting build_followers.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/src/build_followers.py &
fi

# if pgrep -f "new_followers.py" > /dev/null
# then
#     echo "new_followers.py is running."
# else
#     echo "new_followers.py is not running. Starting new_followers.py"
#     /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/src/new_followers.py &
# fi

if /home/$USER/.pyenv/shims/python -f "tweet_metrics.py" > /dev/null
then
    echo "tweet_metrics.py is running."
else
    echo "tweet_metrics.py is not running. Starting tweet_metrics.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/src/tweet_metrics.py &
fi

if pgrep -f "update_summaries.py" > /dev/null
then
    echo "update_summaries.py is running."
else
    echo "update_summaries.py is not running. Starting update_summaries.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/src/update_summaries.py &
fi
