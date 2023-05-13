
import requests
from time import sleep
import mysql.connector
from datetime import datetime
import config

BEARER_TOKEN = config.BEARER_TOKEN
TWITTER_USER_ID = config.TWITTER_USER_ID

MYSQL_HOST = config.MYSQL_HOST
MYSQL_USER = config.MYSQL_USER
MYSQL_PASSWORD = config.MYSQL_PASSWORD
MYSQL_DATABASE = config.MYSQL_DATABASE

FREQUENCY = config.NEW_FOLLOWERS_FREQUENCY

db = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = db.cursor()

def get_user_follower_count():
    url = f"https://api.twitter.com/2/users/{TWITTER_USER_ID}"
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    params = {
        'user.fields': 'public_metrics'
    }
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                # print(response.json())
                return response.json()['data']['public_metrics']['followers_count']
            else:
                if response.status_code == 429:
                    print('rate limited')
                    sleep(5 * 60)
                    continue
                else:
                    print(f"Request returned an error: {response.status_code}, {response.text}")
                    return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

def track_new_followers():
    last_token = get_last_pagination_token()
    url = f"https://api.twitter.com/2/users/{TWITTER_USER_ID}/followers"
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    params = {
        'user.fields': 'public_metrics',
        'max_results': 100,
        'pagination_token': last_token if last_token else None
    }
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                if response.status_code == 429:
                    print('rate limited')
                    sleep(5 * 60)
                    continue
                else:
                    print(f"Request returned an error: {response.status_code}, {response.text}")
                    return
            json_response = response.json()
            followers = json_response['data']
            next_token = json_response['meta']['next_token']
            user_followers_count = get_user_follower_count()
            for follower in followers:
                save_follower_info(follower, user_followers_count, next_token)
            if 'next_token' not in json_response['meta']:
                break
            params['pagination_token'] = next_token
            sleep(FREQUENCY)
        except Exception as e:
            print(f"Exception: {e}")
            return

def get_last_pagination_token():
    select_query = "SELECT pagination_token FROM followers ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
    return result[0] if result else None

def save_follower_info(follower, user_followers_count, next_token):
    now = datetime.now()
    insert_query = """
    INSERT INTO followers (timestamp, twitter_id, username, followers_count, following_count, tweet_count, listed_count, user_followers_count, pagination_token)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE timestamp = VALUES(timestamp), followers_count = VALUES(followers_count), following_count = VALUES(following_count),
    tweet_count = VALUES(tweet_count), listed_count = VALUES(listed_count), user_followers_count = VALUES(user_followers_count), pagination_token = VALUES(pagination_token)
    """
    cursor.execute(insert_query, (now, follower['id'], follower['username'], follower['public_metrics']['followers_count'],
                                  follower['public_metrics']['following_count'], follower['public_metrics']['tweet_count'],
                                  follower['public_metrics']['listed_count'], user_followers_count, next_token))
    db.commit()

while True:
    try:
        track_new_followers()
        sleep(FREQUENCY)
    except Exception as e:
        print(f"Exception: {e}")
        pass
