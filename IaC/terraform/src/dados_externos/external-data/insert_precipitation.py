import pandas as pd
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from os.path import join

from mysql_connection import MysqlConnection
load_dotenv()

df_prec = pd.read_csv('./data/precipitation.csv', sep=',')
df_prec['region'] = 'brazil'
df_prec['date'] = pd.to_datetime(df_prec['date'])

downloads_path = str(join(Path.home(), "Downloads"))
print(f'Downloading dataset precipitation to {downloads_path}...')
df_prec.to_excel(join(downloads_path, 'dataset_precipitation_soybean.xlsx'), index=True)

mysql_connection = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_connection.connect()
mysql_connection.insert_dataframe(df_prec, 'precipitation', 'soybean', index=True)
mysql_connection.disconnect()
