import pandas as pd
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from os.path import join

from mysql_connection import MysqlConnection
load_dotenv()

df_prices = pd.read_csv('./data/Soybean-Price.csv', sep=';')
df_prices['region'] = 'brazil'
df_prices['date'] = pd.to_datetime(df_prices['date'])

df_prices["real"] = df_prices["real"].str.replace(',','.')
df_prices["usd"] = df_prices["usd"].str.replace(',','.')
df_prices['real'] = df_prices['real'].astype('float64')
df_prices['usd'] = df_prices['usd'].astype('float64')

downloads_path = str(join(Path.home(), "Downloads"))
print(f'Downloading dataset prices to {downloads_path}...')
df_prices.to_excel(join(downloads_path, 'dataset_prices_soybean.xlsx'), index=True)

mysql_connection = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_connection.connect()
mysql_connection.insert_dataframe(df_prices, 'prices', 'soybean', index=True)
mysql_connection.disconnect()
