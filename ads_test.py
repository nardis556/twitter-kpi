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

url = "https://ads-api.twitter.com/7/stats/accounts/your_ads_account_id/active_entities?"