import pandas as pd
from os import getenv
from dotenv import load_dotenv; load_dotenv()
from pathlib import Path
from os.path import join

from mysql_connection import MysqlConnection

def format_date(row):
    date = str(row['date'])
    date = date.replace('-', '/')
    return date

df = pd.read_csv('./data/california_weather.csv', sep=',')

df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
df['date'] = df.apply(lambda row: format_date(row), axis=1)

print(df.head())

downloads_path = str(join(Path.home(), "Downloads"))
print(f'Downloading dataset temperature_california to {downloads_path}...')
df.to_excel(join(downloads_path, 'temperature_california.xlsx'), index=True)

mysql_db = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_db.connect()
mysql_db.insert_dataframe(df, 'temperature_california', 'soybean', index=True)
mysql_db.disconnect()
