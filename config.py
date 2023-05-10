
## TWITTER CONFIG
BEARER_TOKEN = ''
TWITTER_USER_ID = '' # TWITTER USER ID TO FETCH FOLLOWERS

## MYSQL CONFIG
MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''

## FREQUENCY CONFIGS

## FOLLOWERS
NEW_FOLLOWERS_FREQUENCY = 20 # seconds | NOT YET CONFIGURED IN SCRIPT
BUILD_FOLLOWERS_FREQUENCY = 5 # minutes

## SEARCH TWEETS
SEARCH_TWEETS_FREQUENCY = 2 # minutes
QUERY = '<QUERY TWITTER USERNAME>'

# UPDATES ROWS BASED ON INTERVAL
SEARCH_UPDATE_INTERVAL = [
    (6, 12, 1),
    (12, 24, 2),
    (24, 48, 3),
]
