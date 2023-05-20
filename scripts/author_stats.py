

from time import time, sleep
import requests
import mysql.connector
from datetime import datetime
import config

BEARER_TOKEN = config.BEARER_TOKEN
TWITTER_USER_ID = config.TWITTER_USER_ID

MYSQL_HOST = config.MYSQL_HOST
MYSQL_USER = config.MYSQL_USER
MYSQL_PASSWORD = config.MYSQL_PASSWORD
MYSQL_DATABASE = config.MYSQL_DATABASE

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = db.cursor()

def main():
    url = f"https://api.twitter.com/2/users/{TWITTER_USER_ID}"
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    params = {
        'user.fields': 'public_metrics',
    }
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()['data']['public_metrics']
                followers_count = data['followers_count']
                following_count = data['following_count']
                tweet_count = data['tweet_count']
                listed_count = data['listed_count']

                # print(data)

                cursor.execute(
                    "INSERT INTO author (followers_count, following_count, tweet_count, listed_count, timestamp) VALUES (%s, %s, %s, %s, %s)",
                    (followers_count, following_count, tweet_count, listed_count, datetime.now())
                )
                db.commit()

                return followers_count, following_count, tweet_count, listed_count
            else:
                if response.status_code == 429:
                    rate_limit_remaining = int(response.headers.get('x-rate-limit-remaining', 0))
                    rate_limit_reset = int(response.headers.get('x-rate-limit-reset', 0))
                    if rate_limit_remaining == 0:
                        sleep_time = rate_limit_reset - time() + 5
                        # print(f'Rate limited. Waiting for {sleep_time} seconds before retrying.')
                        sleep(sleep_time)
                    continue  
                else:
                    # print(f"Request returned an error: {response.status_code}, {response.text}")
                    return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

main()
