import pandas as pd
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from os.path import join

from mysql_connection import MysqlConnection
load_dotenv()

df_export = pd.read_csv('./data/exportacao_soja_15_19.csv', sep=',')
df_export.drop(['CO_NCM', 'CO_UNID', 'CO_PAIS', 
                'CO_VIA', 'CO_URF', 'QT_ESTAT', 
                'VL_FOB', 'Unnamed: 0'], axis = 1, inplace = True)
df_export['date'] = df_export['CO_MES'].astype(str).str.zfill(2) + '/' + df_export['CO_ANO'].astype(str)
df_export['date'] = pd.to_datetime(df_export['date'])
del df_export['CO_ANO']
del df_export['CO_MES']
df_export.rename(columns={'SG_UF_NCM': 'state', 'KG_LIQUIDO': 'kg'}, inplace=True)
df_export['region'] = 'brazil'

print(df_export.head())

downloads_path = str(join(Path.home(), "Downloads"))
print(f'Downloading dataset export to {downloads_path}...')
df_export.to_excel(join(downloads_path, 'dataset_export_soybean.xlsx'), index=True)

mysql_connection = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_connection.connect()
mysql_connection.insert_dataframe(df_export, 'exportation', 'soybean', index=True)
mysql_connection.disconnect()
