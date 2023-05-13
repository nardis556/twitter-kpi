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


tweet_id = "1657028489546014722"

tweet_url = f"https://api.twitter.com/2/tweets/{tweet_id}"
headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
}
params = {
    'tweet.fields': 'public_metrics,created_at',
}
response = requests.get(tweet_url, headers=headers, params=params)

print(response.json())