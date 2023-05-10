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

FREQUENCY = config.BUILD_FOLLOWERS_FREQUENCY # minutes


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
                # print(response.json()['data']['public_metrics']['followers_count'])
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

def get_all_followers(last_pagination_token):
    url = f"https://api.twitter.com/2/users/{TWITTER_USER_ID}/followers"
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    params = {
        'user.fields': 'public_metrics',
        'max_results': 50,
        'pagination_token': last_pagination_token
    }
    
    all_followers = []
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Request returned an error: {response.status_code}, {response.text}")
                if response.status_code == 429:
                    print("rate limited")
                    sleep(5 * 60)
                    continue
                else:
                    break
            json_response = response.json()
            all_followers.extend(json_response['data'])
            if 'next_token' not in json_response['meta']:
                break
            params['pagination_token'] = json_response['meta']['next_token']
        except Exception as e:
            print(f"Exception: {e}")
            break
    return all_followers, params.get('pagination_token', None)



def get_last_pagination_token():
    select_query = "SELECT pagination_token FROM followers ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
    # print(result)
    return result[0] if result else None


def save_follower_info(follower, user_followers_count, pagination_token):
    now = datetime.now()
    select_query = "SELECT 1 FROM followers WHERE twitter_id = %s"
    cursor.execute(select_query, (follower['id'],))
    if cursor.fetchone() is None:
        insert_query = """
        INSERT INTO followers (timestamp, twitter_id, username, followers_count, following_count, tweet_count, listed_count, user_followers_count, pagination_token)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (now, follower['id'], follower['username'], follower['public_metrics']['followers_count'],
                                      follower['public_metrics']['following_count'], follower['public_metrics']['tweet_count'],
                                      follower['public_metrics']['listed_count'], user_followers_count, pagination_token))
        db.commit()


def track_followers():
    last_pagination_token = get_last_pagination_token()
    all_followers, next_pagination_token = get_all_followers(last_pagination_token)
    user_followers_count = get_user_follower_count()
    for follower in all_followers:
        # print(follower)
        save_follower_info(follower, user_followers_count, next_pagination_token)


while True:
    try:
        track_followers()
        sleep(FREQUENCY * 60)
    except Exception as e:
        print(f"Exception: {e}")
        pass
