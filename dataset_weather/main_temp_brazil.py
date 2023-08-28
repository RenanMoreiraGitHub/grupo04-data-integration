import pandas as pd
from os import getenv
from dotenv import load_dotenv; load_dotenv()

from mysql_connection import MysqlConnection

hour_formatter = {
    '0': '00:00:00',
    '1200': '12:00:00',
    '1800': '18:00:00'
}

def format_hour(row):
    date = str(row['Data'])
    unformatted_hour = str(row['Hora'])
    return date + ' ' + hour_formatter[unformatted_hour]

df = pd.read_csv('./data/conventional_weather_stations_inmet_brazil_1961_2019.csv', sep=',')
df.fillna(method='ffill', inplace=True)
df.fillna(method='bfill', inplace=True)
df['date'] = df.apply(lambda row: format_hour(row), axis=1)
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M:%S')
df.drop(['Data', 'Hora'], axis = 1, inplace = True)

print(df.head())

mysql_db = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_db.connect()
mysql_db.insert_dataframe(df, 'temperature_brazil', 'soybean', index=True)
mysql_db.disconnect()
