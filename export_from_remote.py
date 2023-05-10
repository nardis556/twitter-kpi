# run in cron

import mysql.connector
import config

config_remote = {
    'host': config.REMOTE_MYSQL_HOST,
    'user': config.REMOTE_MYSQL_USER,
    'password': config.REMOTE_MYSQL_PASSWORD,
    'database': config.REMOTE_MYSQL_DATABASE
}

config_local = {
    'host': config.MYSQL_HOST,
    'user': config.MYSQL_USER,
    'password': config.MYSQL_PASSWORD,
    'database': config.MYSQL_DATABASE
}

remote_db = mysql.connector.connect(**config_remote)
remote_cursor = remote_db.cursor()

local_db = mysql.connector.connect(**config_local)
local_cursor = local_db.cursor()

local_cursor.execute("SELECT MAX(tweet_id) FROM twitter")
result = local_cursor.fetchone()
latest_tweet_id_local = result[0] if result else None

if latest_tweet_id_local:
    remote_cursor.execute(f"SELECT * FROM twitter WHERE tweet_id > {latest_tweet_id_local}")
else:
    remote_cursor.execute("SELECT * FROM twitter")

new_tweets = remote_cursor.fetchall()

for tweet in new_tweets:
    placeholders = ', '.join(['%s'] * len(tweet))
    query = f"INSERT INTO twitter VALUES ({placeholders})"
    local_cursor.execute(query, tweet)
    local_db.commit()
    
remote_cursor.close()
remote_db.close()
local_cursor.close()
local_db.close()
