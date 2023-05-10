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
SEARCH_FROM_QUERY = f'from:{QUERY}'

SEARCH_MENTIONS_QUERY = f'(@{QUERY} OR #{QUERY})'



SEARCH_FREQUENCY = config.SEARCH_TWEETS_FREQUENCY


headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}',
}


params = {  # param for new tweet
    'query': SEARCH_FROM_QUERY,
    'tweet.fields': 'public_metrics,created_at',
    'expansions': 'author_id,in_reply_to_user_id,referenced_tweets.id',
    'user.fields': 'username',
    'max_results': 100,
}


url = 'https://api.twitter.com/2/tweets/search/recent'


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


print(
    f'''

    STARTING TWEET SEARCHER
    
    ## CONFIG

    MYSQL_HOST:         {MYSQL_HOST}
    MYSQL_USER:         {MYSQL_USER}
    MYSQL_DATABASE:     {MYSQL_DATABASE}

    Cooldown:           {SEARCH_FREQUENCY} minutes


    '''
)


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def get_last_tweet_timestamp(author=None):
    # print("Executing get_last_tweet_timestamp()")
    if author == QUERY:
        query = f"SELECT MAX(timestamp) FROM twitter WHERE author = '{QUERY}'"
        # print(query)
    elif author == f'!{QUERY}':
        query = f"SELECT MAX(timestamp) FROM twitter WHERE author != '{QUERY}'"
        # print(query)
    else:
        query = "SELECT MAX(timestamp) FROM twitter"
        # print(query)
    cursor.execute(query)
    result = cursor.fetchone()
    # print("get_last_tweet_timestamp() executed successfully")
    # # print(result[0])
    return result[0]


latest_tweet = {f'from_{QUERY}': None, f'!{QUERY}': None}


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def is_tweet_in_db(tweet_id, message, query_type):
    # print(f"Executing is_tweet_in_db() for tweet_id {tweet_id}")

    if tweet_id == latest_tweet[query_type]:
        # print(f"Tweet ID {tweet_id} found in the latest_tweet for query_type {query_type}")
        return (tweet_id,)

    query = "SELECT tweet_id, message FROM twitter WHERE tweet_id = %s OR message = %s"
    cursor.execute(query, (tweet_id, message))
    result = cursor.fetchone()
    # print(f"is_tweet_in_db() executed successfully for tweet_id {tweet_id}")

    if result:
        latest_tweet[query_type] = tweet_id

    return result if result else None


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def update_old_tweets():
    # print("Executing update_old_tweets()")
    now = datetime.datetime.now()
    update_intervals = [
        (6, 12, 1),
        (12, 24, 2),
        (24, 48, 3),
    ]
    for start_hours, end_hours, updated_value in update_intervals:
        start_time = now - datetime.timedelta(hours=end_hours)
        end_time = now - datetime.timedelta(hours=start_hours)
        query = '''
        SELECT tweet_id FROM twitter
        WHERE updated < %s AND timestamp > %s AND timestamp < %s AND (updated_time < %s OR updated_time IS NULL)
        '''
        cursor.execute(
            query, (updated_value, start_time, end_time, start_time))
        old_tweet_ids = cursor.fetchall()
        for (tweet_id,) in old_tweet_ids:
            tweet_data = get_tweet_data(tweet_id)
            if tweet_data:
                query = '''
                UPDATE twitter SET likes = %s, retweets = %s, replies = %s, quotes = %s, impressions = %s, updated = %s, updated_time = %s
                WHERE tweet_id = %s
                '''
                values = (
                    tweet_data['like_count'], tweet_data['retweet_count'],
                    tweet_data['reply_count'], tweet_data['quote_count'],
                    tweet_data['impression_count'],
                    updated_value,
                    now,
                    tweet_id
                )
                cursor.execute(query, values)
                db.commit()
                # print(f"Tweet ID: {tweet_id} updated with value {updated_value}")

    # print("update_old_tweets() executed successfully")


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def get_tweet_data(tweet_id):
    # print(f"Executing get_tweet_data() for tweet_id {tweet_id}")
    tweet_url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    params = {
        'tweet.fields': 'public_metrics,created_at',
    }
    response = requests.get(tweet_url, headers=headers, params=params)
    
    if response.status_code == 200:
        rate_limit_remaining = int(response.headers.get('x-rate-limit-remaining', 0))
        rate_limit_reset = int(response.headers.get('x-rate-limit-reset', 0))
        if rate_limit_remaining == 0:
            sleep_time = rate_limit_reset - time() + 5  # adding a buffer of 5 seconds
            sleep(sleep_time)
        
        data = response.json()
        if 'data' in data:
            # print(f"get_tweet_data() executed successfully for tweet_id {tweet_id}")
            return data['data']['public_metrics']
        else:
            # print(f"No 'data' field in response for tweet_id {tweet_id}")
            return None
    else:
        # print(f"Error fetching tweet data: {response.status_code} - {response.text}")
        return None


def main():
    update_old_tweets()
    # print("Old tweets updated.")
    for query_type in [SEARCH_FROM_QUERY, SEARCH_MENTIONS_QUERY]:
        # print("Getting last tweet timestamp...")
        if query_type == f'from:{QUERY}':
            last_tweet_timestamp = get_last_tweet_timestamp(f'{QUERY}')
        else:
            last_tweet_timestamp = get_last_tweet_timestamp(f'!{QUERY}')
        # print(f"Last tweet timestamp: {last_tweet_timestamp}")
        if last_tweet_timestamp:
            params['start_time'] = last_tweet_timestamp.strftime(
                '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        else:
            params['start_time'] = '2023-05-02T18:00:00.000Z'
        # print(f"Requesting recent tweets with query: {query_type}")
        params['query'] = query_type
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            rate_limit_remaining = int(response.headers.get('x-rate-limit-remaining', 0))
            rate_limit_reset = int(response.headers.get('x-rate-limit-reset', 0))
            if rate_limit_remaining == 0:
                sleep_time = rate_limit_reset - time.time() + 5  # adding a buffer of 5 seconds
                sleep(sleep_time)
            # print("Recent tweets received")
            data = response.json()
            if data['meta']['result_count'] > 0:
                tweets = data['data']
                users = {user['id']: user['username']
                         for user in data['includes']['users']}
                for tweet in tweets:
                    tweet_id = tweet['id']
                    text = tweet['text']
                    tweet_author = users[tweet['author_id']]
                    tweet_timestamp = datetime.datetime.fromisoformat(
                        tweet['created_at'].replace('Z', '+00:00'))
                    referenced_tweets = tweet.get('referenced_tweets', [])
                    replied_to_id = None
                    quoted_id = None
                    retweeted_id = None
                    # print(tweet)
                    # print(tweet['data'])
                    for ref_tweet in referenced_tweets:
                        # print(ref_tweet['id'])
                        if ref_tweet['type'] == 'replied_to':
                            replied_to_id = ref_tweet['id']
                        elif ref_tweet['type'] == 'quoted':
                            quoted_id = ref_tweet['id']
                        elif ref_tweet['type'] == 'retweeted':
                            retweeted_id = ref_tweet['id']
                    replied_to_user = None
                    if replied_to_id:
                        replied_to_user_id = tweet.get(
                            'in_reply_to_user_id', None)
                        if replied_to_user_id:
                            replied_to_user = users.get(
                                replied_to_user_id, None)
                    # print(tweet['public_metrics']']
                    metrics = tweet['public_metrics']
                    likes = metrics['like_count']
                    retweets = metrics['retweet_count']
                    replies = metrics['reply_count']
                    quotes = metrics['quote_count']
                    if query_type == SEARCH_MENTIONS_QUERY:
                        if text.startswith('RT @'):
                            continue
                        elif f'@{QUERY}' in text or f'#{QUERY}' in text:
                            tweet_type = 'mentions'
                    elif text.startswith('RT @'):
                        tweet_type = 'retweet'
                    elif text.startswith('@'):
                        tweet_type = 'reply'
                    else:
                        tweet_type = 'original'
                    existing_tweet = is_tweet_in_db(
                        tweet_id, text, f'from_{QUERY}' if query_type == f'from:{QUERY}' else f'!{QUERY}')
                    if not existing_tweet:
                        metrics = tweet['public_metrics']
                        query = '''
                        INSERT INTO twitter (tweet_id, tweet_type, author, message, likes, retweets, replies, quotes, impressions, timestamp, replied_to_id, quoted_id, replied_to_user, retweet_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        '''
                        values = (
                            tweet_id, tweet_type, tweet_author, text,
                            likes, retweets, replies, quotes,
                            metrics['impression_count'],
                            tweet_timestamp,
                            replied_to_id, quoted_id, replied_to_user, retweeted_id
                        )
                        cursor.execute(query, values)
                        db.commit()
                        # print(f"Tweet ID: {tweet_id} added as {tweet_type}")
                        sleep(0.05)
                    else:
                        if existing_tweet[0] != tweet_id:
                            query = '''
                            UPDATE twitter SET dupli_message = 1
                            WHERE tweet_id = %s
                            '''
                            cursor.execute(query, (existing_tweet[0],))
                            db.commit()
                            # print(f"Tweet with duplicate message found, tweet ID: {existing_tweet[0]} updated")
            else:
                print("No new tweets found")
            sleep(5)
        else:
            print(f"Error: {response.status_code} - {response.text}")
        # print("Main function completed")


class Signal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\b' * len(status))
        sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\b' * len(status))


def stop_spinner(signal):
    signal.go = False

sleep(2)

signal = Signal()
spinner = threading.Thread(target=spin, args=("TWEET SEARCHER RUNNING...", signal))
spinner.start()


try:
    while True:
        main()
        sleep(SEARCH_FREQUENCY * 60)
except Exception as e:
    traceback.print_exc()
    pass
finally:
    # stop spinner
    stop_spinner(signal)
    spinner.join()
