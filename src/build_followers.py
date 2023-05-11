import requests
from time import sleep, time
import mysql.connector
from datetime import datetime
import config
from tenacity import retry, stop_after_attempt, wait_fixed
import threading
import itertools
import sys

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


def prepare_request_data(pagination_token=None, max_results=None, user_fields='public_metrics'):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    params = {
        'user.fields': user_fields,
    }
    if pagination_token:
        params['pagination_token'] = pagination_token
    if max_results:
        params['max_results'] = max_results
    
    return headers, params


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def get_all_followers(last_pagination_token):
    # print('get_all_followers')
    url = f"https://api.twitter.com/2/users/{TWITTER_USER_ID}/followers"
    headers, params = prepare_request_data(last_pagination_token, config.RETURNED_FOLLOWERS_COUNT)
    
    all_followers = []
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            # print(response)
            if response.status_code != 200:
                # print(f"Request returned an error: {response.status_code}, {response.text}")
                if response.status_code == 429:
                    # print(int(response.headers.get('x-rate-limit-remaining', 0)))
                    # print(int(response.headers.get('x-rate-limit-reset', 0)))
                    # print("rate limited")
                    rate_limit_remaining = int(response.headers.get('x-rate-limit-remaining', 0))
                    rate_limit_reset = int(response.headers.get('x-rate-limit-reset', 0))
                    if rate_limit_remaining == 0:
                        sleep_time = rate_limit_reset - time() + 5
                        sleep(sleep_time)
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


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def get_user_follower_count():
    # print('get_user_follower_count')
    url = f"https://api.twitter.com/2/users/{TWITTER_USER_ID}"
    headers, params = prepare_request_data()
    
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            # print(response)
            if response.status_code == 200:
                return response.json()['data']['public_metrics']['followers_count']
            else:
                if response.status_code == 429:
                    # print(int(response.headers.get('x-rate-limit-remaining', 0)))
                    # print(int(response.headers.get('x-rate-limit-reset', 0)))
                    # print('rate limited')
                    rate_limit_remaining = int(response.headers.get('x-rate-limit-remaining', 0))
                    rate_limit_reset = int(response.headers.get('x-rate-limit-reset', 0))
                    if rate_limit_remaining == 0:
                        sleep_time = rate_limit_reset - time() + 5 
                        sleep(sleep_time)
                    continue
                else:
                    # print(f"Request returned an error: {response.status_code}, {response.text}")
                    return None
        except Exception as e:
            print(f"Exception: {e}")
            return None


def get_last_pagination_token():
    select_query = "SELECT pagination_token FROM followers ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
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

count = 0

def main():
    global count
    print(count++1)
    last_pagination_token = get_last_pagination_token()
    all_followers, next_pagination_token = get_all_followers(last_pagination_token)
    user_followers_count = get_user_follower_count()
    for follower in all_followers:
        save_follower_info(follower, user_followers_count, next_pagination_token)


while True:
    try:
        main()
        sleep(FREQUENCY * 60)
    except Exception as e:
        print(f"Exception: {e}")
        pass

# class Signal:
#     go = True


# def spin(msg, signal):
#     write, flush = sys.stdout.write, sys.stdout.flush
#     for char in itertools.cycle('|/-\\'):
#         status = char + ' ' + msg
#         write(status)
#         flush()
#         write('\b' * len(status))
#         sleep(.1)
#         if not signal.go:
#             break
#     write(' ' * len(status) + '\b' * len(status))


# def stop_spinner(signal):
#     signal.go = False

# sleep(2)

# signal = Signal()
# spinner = threading.Thread(target=spin, args=("BUILDING FOLLOWERS...", signal))
# spinner.start()


# try:
#     while True:
#         main()
#         sleep(FREQUENCY * 60)
# except Exception as e:
#     # traceback.print_exc()
#     pass
# finally:
#     # stop spinner
#     stop_spinner(signal)
#     spinner.join()

