#!/bin/bash

sleep 10

if pgrep -f "build_followers.py" > /dev/null
then
    echo "build_followers.py is running."
else
    echo "build_followers.py is not running. Starting build_followers.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/build_followers.py &
fi

# if pgrep -f "new_followers.py" > /dev/null
# then
#     echo "new_followers.py is running."
# else
#     echo "new_followers.py is not running. Starting new_followers.py"
#     /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/new_followers.py &
# fi

if pgrep -f "tweet_metrics.py" > /dev/null
then
    echo "tweet_metrics.py is running."
else
    echo "tweet_metrics.py is not running. Starting tweet_metrics.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/tweet_metrics.py &
fi

if pgrep -f "update_summaries.py" > /dev/null
then
    echo "update_summaries.py is running."
else
    echo "update_summaries.py is not running. Starting update_summaries.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/update_summaries.py &
fi

if pgrep -f "author_engagements.py" > /dev/null
then
    echo "author_engagements.py is running."
else
    echo "author_engagements.py is not running. Starting author_engagements.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/author_engagements.py &
fi

if pgrep -f "user_engagements.py" > /dev/null
then
    echo "user_engagements.py is running."
else
    echo "user_engagements.py is not running. Starting user_engagements.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/user_engagements.py &
fi

if pgrep -f "author_stats.py" > /dev/null
then
    echo "author_stats.py is running."
else
    echo "author_stats.py is not running. Starting author_stats.py"
    /home/$USER/.pyenv/shims/python /home/$USER/twitter-kpi/scripts/author_stats.py &
fi

