from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import mysql.connector
import config
import time
import traceback


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

def start_of_week(dt):
    return dt - timedelta(days=dt.weekday())

def start_of_month(dt):
    return dt.replace(day=1)

def update_summaries(interval):
    for tweet_type in ['original', 'retweet', 'reply', 'mentions']:
        end_date = datetime.now()
        if interval == 'daily':
            start_date = end_date - relativedelta(days=1)
            group_by_clause = "DATE(timestamp)"
        elif interval == 'weekly':
            start_date = end_date - relativedelta(weeks=1)
            group_by_clause = "STR_TO_DATE(CONCAT(YEARWEEK(timestamp), ' Sunday'), '%X%V %W')"
        elif interval == 'monthly':
            start_date = end_date - relativedelta(months=1)
            group_by_clause = "DATE_FORMAT(timestamp, '%Y-%m-01')"

        print(tweet_type, start_date, end_date)

        query = f"""
            INSERT INTO {interval}_summary_{tweet_type} (date, likes, retweets, replies, quotes, impressions)
            SELECT 
                {group_by_clause},
                SUM(likes), 
                SUM(retweets),
                SUM(replies),
                SUM(quotes),
                SUM(impressions)
            FROM twitter
            WHERE 
                tweet_type = '{tweet_type}' AND 
                timestamp BETWEEN '{start_date.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_date.strftime('%Y-%m-%d %H:%M:%S')}'
            GROUP BY {group_by_clause}
            ON DUPLICATE KEY UPDATE
                likes = VALUES(likes),
                retweets = VALUES(retweets),
                replies = VALUES(replies),
                quotes = VALUES(quotes),
                impressions = VALUES(impressions)
        """

        cursor.execute(query)
        db.commit()

while True:
  try:
    update_summaries('daily')
    time.sleep(60)
    update_summaries('weekly')
    time.sleep(60)
    update_summaries('monthly')
    time.sleep(21600)
  except Exception as e:
    traceback.print_exc()
    pass
