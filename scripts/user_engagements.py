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

def update_user_engagement_summaries(interval):
    cursor.execute(f"SELECT MAX(date) FROM user_{interval}_engagements")
    start_date = cursor.fetchone()[0]
    if start_date is None:
        cursor.execute(f"SELECT MIN(timestamp) FROM twitter")
        start_date = cursor.fetchone()[0]
    else:
        if (datetime.now().date() - start_date).days < 7:
            start_date = datetime.now().date() - timedelta(days=7)
        else:
            start_date = start_date + relativedelta(days=1)
    end_date = datetime.now()
    if interval == 'daily':
        group_by_clause = "DATE(timestamp)"
    elif interval == 'weekly':
        start_date = start_of_week(start_date)
        group_by_clause = "STR_TO_DATE(CONCAT(YEARWEEK(timestamp), ' Sunday'), '%X%V %W')"
    elif interval == 'monthly':
        start_date = start_of_month(start_date)
        group_by_clause = "DATE_FORMAT(timestamp, '%Y-%m-01')"
    query = f"""
        INSERT INTO user_{interval}_engagements (username, date, engagements)
        SELECT 
            author,
            {group_by_clause},
            COUNT(author) AS engagements
        FROM twitter
        WHERE 
            timestamp BETWEEN '{start_date.strftime('%Y-%m-%d %H:%M:%S')}' AND '{end_date.strftime('%Y-%m-%d %H:%M:%S')}'
        GROUP BY author, {group_by_clause}
        ON DUPLICATE KEY UPDATE
            engagements = VALUES(engagements)
    """

    cursor.execute(query)
    db.commit()

while True:
  try:
    update_user_engagement_summaries('daily')
    time.sleep(5)
    update_user_engagement_summaries('weekly')
    time.sleep(5)
    update_user_engagement_summaries('monthly')
    time.sleep(config.SQL_QUERY_FREQUENCY * 60)
  except Exception as e:
    traceback.print_exc()
    pass
