import pandas as pd
from os import getenv
from dotenv import load_dotenv; load_dotenv()

from mysql_connection import MysqlConnection

def format_date(row):
    date = str(row['date'])
    date = date.replace('-', '/')
    return date

df = pd.read_csv('./data/california_weather.csv', sep=',')

df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
df['date'] = df.apply(lambda row: format_date(row), axis=1)

print(df.head())

mysql_db = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_db.connect()
mysql_db.insert_dataframe(df, 'temperature_california', 'soybean', index=True)
mysql_db.disconnect()
