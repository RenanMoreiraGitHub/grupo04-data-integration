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

region_mapping = {
    'AC': 'Norte',
    'AL': 'Nordeste',
    'AP': 'Norte',
    'AM': 'Norte',
    'BA': 'Nordeste',
    'CE': 'Nordeste',
    'DF': 'Centro Oeste',
    'ES': 'Sudeste',
    'GO': 'Centro Oeste',
    'MA': 'Nordeste',
    'MT': 'Centro Oeste',
    'MS': 'Centro Oeste',
    'MG': 'Sudeste',
    'PA': 'Norte',
    'PB': 'Nordeste',
    'PR': 'Sul',
    'PE': 'Nordeste',
    'PI': 'Nordeste',
    'RJ': 'Sudeste',
    'RN': 'Nordeste',
    'RS': 'Sul',
    'RO': 'Norte',
    'RR': 'Norte',
    'SC': 'Sul',
    'SP': 'Sudeste',
    'SE': 'Nordeste',
    'TO': 'Norte'
}
acronym_mapping = {
    'Sul': 'S',
    'Norte': 'N',
    'Sudeste': 'SE',
    'Nordeste': 'NE',
    'Centro Oeste': 'CO',
}

def map_to_region(state):
    return region_mapping.get(state, 'Outro')
def map_to_acronym(region):
    return acronym_mapping.get(region, 'Outro')

df_export['region'] = df_export['state'].apply(map_to_region)
df_export['acronym'] = df_export['region'].apply(map_to_acronym)

print(df_export.head(30))

downloads_path = str(join(Path.home(), "Downloads"))
print(f'Downloading dataset export to {downloads_path}...')
df_export.to_excel(join(downloads_path, 'dataset_export_soybean.xlsx'), index=True)

mysql_connection = MysqlConnection(
    getenv('USER_BD'), getenv('PASS_BD'), getenv('HOST_BD'))
mysql_connection.connect()
mysql_connection.insert_dataframe(df_export, 'exportation', 'soybean', index=True)
mysql_connection.disconnect()
