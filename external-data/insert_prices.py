import pandas as pd
from os import getenv
from dotenv import load_dotenv

from mysql_connection import MysqlConnection
load_dotenv()

df_prices = pd.read_csv('./data/Soybean-Price.csv', sep=';')
df_prices['region'] = 'brazil'
df_prices['date'] = pd.to_datetime(df_prices['date'])

mysql_connection = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_connection.connect()
mysql_connection.insert_dataframe(df_prices, 'prices', 'soybean', index=True)
mysql_connection.disconnect()
