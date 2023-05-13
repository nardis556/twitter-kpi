import requests
import datetime
import mysql.connector
from time import sleep, time
import traceback
import config
from tenacity import retry, stop_after_attempt, wait_fixed
import threading
import itertools
import sys


BEARER_TOKEN = config.BEARER_TOKEN

QUERY = config.QUERY
ADD_QUERY = config.ADD_QUERY

SEARCH_FROM_QUERY = f'from:{QUERY}'


def get_search_mentinos():
    if ADD_QUERY != '' or not None:
        return f'(@{QUERY} OR #{QUERY} OR ${ADD_QUERY} OR #{ADD_QUERY})'
    else:
        return f'(@{QUERY} OR #{QUERY})'

print(get_search_mentinos())

headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
}


params = {  # param for new tweet
    'query': SEARCH_FROM_QUERY,
    'tweet.fields': 'public_metrics,created_at',
    'expansions': 'author_id,in_reply_to_user_id,referenced_tweets.id',
    'user.fields': 'username',
    'max_results': 100,
    'start_time': '2023-05-12T17:00:00.000Z'
}


url = 'https://api.twitter.com/2/tweets/search/recent'

response = requests.get(url, headers=headers, params=params)
print(response.json())