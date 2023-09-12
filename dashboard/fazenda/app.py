import pandas as pd
import streamlit as st
import src.pages.history_sensors as h_sensors


def sensors_history():
    df_anemometro = pd.read_parquet('./datasets/df_anemometro.parquet')
    df_anemometro['Dia'] = pd.to_datetime(df_anemometro['data_hora'])
    df_anemometro['Mes'] = df_anemometro['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_anemometro['Ano'] = df_anemometro['Dia'].apply(lambda x: str(x.year))

    df_bmp = pd.read_parquet('./datasets/df_bmp.parquet')
    df_bmp['Dia'] = pd.to_datetime(df_bmp['data_hora'])
    df_bmp['Mes'] = df_bmp['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_bmp['Ano'] = df_bmp['Dia'].apply(lambda x: str(x.year))

    df_dht = pd.read_parquet('./datasets/df_dht.parquet')
    df_dht['Dia'] = pd.to_datetime(df_dht['data_hora'])
    df_dht['Mes'] = df_dht['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_dht['Ano'] = df_dht['Dia'].apply(lambda x: str(x.year))

    df_npk = pd.read_parquet('./datasets/df_npk.parquet')
    df_npk['Dia'] = pd.to_datetime(df_npk['data_hora'])
    df_npk['Mes'] = df_npk['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_npk['Ano'] = df_npk['Dia'].apply(lambda x: str(x.year))

    df_tcrt = pd.read_parquet('./datasets/df_tcrt.parquet')
    df_tcrt['Dia'] = pd.to_datetime(df_tcrt['data_hora'])
    df_tcrt['Mes'] = df_tcrt['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_tcrt['Ano'] = df_tcrt['Dia'].apply(lambda x: str(x.year))

    df_umigrain = pd.read_parquet('./datasets/df_umigrain.parquet')
    df_umigrain['Dia'] = pd.to_datetime(df_umigrain['data_hora'])
    df_umigrain['Mes'] = df_umigrain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_umigrain['Ano'] = df_umigrain['Dia'].apply(lambda x: str(x.year))

    h_sensors.render(df_anemometro, df_bmp, df_dht, df_npk, df_tcrt, df_umigrain)


pages = {
    'Histórico dos sensores': sensors_history,
}

page = st.sidebar.selectbox('Selecione uma página', list(pages.keys()))

pages[page]()