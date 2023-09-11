import pandas as pd
import streamlit as st

import src.pages.history_exportation as h_exportation
import src.pages.history_rain as h_rain
import src.pages.history_climate as h_climate
import src.pages.history_price as h_price
import src.pages.correlation as correlation


def export_history():
    df_export = pd.read_csv('datasets\dataset_export_soybean.csv')[['state','kg','date']]
    df_export = df_export.sort_values(by=['date']).reset_index(drop=True)
    df_export['Dia'] = pd.to_datetime(df_export['date'])
    df_export['Mes'] = df_export['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_export['Ano'] = df_export['Dia'].apply(lambda x: str(x.year))
    
    h_exportation.render(df_export)

def rain_history():
    df_rain = pd.read_csv('datasets\dataset_precipitation_soybean.csv')[['state','date','precipitation']]
    df_rain['precipitation'] = df_rain['precipitation'].str.replace(',','.').astype(float)
    df_rain['Dia'] = pd.to_datetime(df_rain['date'])
    df_rain['Mes'] = df_rain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_rain['Ano'] = df_rain['Dia'].apply(lambda x: str(x.year))

    h_rain.render(df_rain)

def climate_history():
    df_climate = pd.read_csv(r'datasets\temperature_brazil.csv')[['TempBulboSeco','TempBulboUmido','TempMaxima',
                                                                 'TempMinima','UmidadeRelativa','date']]
    df_climate['TempBulboSeco'] = df_climate['TempBulboSeco'].str.replace(',', '.').astype(float)
    df_climate['TempBulboUmido'] = df_climate['TempBulboUmido'].str.replace(',', '.').astype(float)
    df_climate['TempMaxima'] = df_climate['TempMaxima'].str.replace(',', '.').astype(float)
    df_climate['TempMinima'] = df_climate['TempMinima'].str.replace(',', '.').astype(float)
    df_climate['UmidadeRelativa'] = df_climate['UmidadeRelativa'].astype(int)

    df_climate['Temperature'] = (df_climate['TempBulboSeco'] + df_climate['TempBulboUmido']) / 2
    df_climate = df_climate[['Temperature','TempMaxima','TempMinima','UmidadeRelativa','date']]

    df_climate['Dia'] = pd.to_datetime(df_climate['date'])
    df_climate['Mes'] = df_climate['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_climate['Ano'] = df_climate['Dia'].apply(lambda x: str(x.year))

    h_climate.render(df_climate)

def money_history():
    df_money = pd.read_csv('datasets\dataset_prices_soybean.csv')[['date','real','usd']]
    df_money['Dia'] = pd.to_datetime(df_money['date'])
    df_money['Mes'] = df_money['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_money['Ano'] = df_money['Dia'].apply(lambda x: str(x.year))

    df_money['real'] = df_money['real'].str.replace(',','.').astype(float)
    df_money['usd'] = df_money['usd'].str.replace(',','.').astype(float)

    h_price.render(df_money)

def analysis():
    df_export = pd.read_csv('datasets\dataset_export_soybean.csv')[['state','kg','date']]
    df_export = df_export.sort_values(by=['date']).reset_index(drop=True)
    df_export['Dia'] = pd.to_datetime(df_export['date'])
    df_export['Mes'] = df_export['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_export['Ano'] = df_export['Dia'].apply(lambda x: str(x.year))
    df_export = df_export.loc[~df_export['state'].isin(['RO', 'MS', 'ND'])]


    df_rain = pd.read_csv('datasets\dataset_precipitation_soybean.csv')[['state','date','precipitation']]
    df_rain['precipitation'] = df_rain['precipitation'].str.replace(',','.').astype(float)
    df_rain['Dia'] = pd.to_datetime(df_rain['date'])
    df_rain['Mes'] = df_rain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_rain['Ano'] = df_rain['Dia'].apply(lambda x: str(x.year))
    df_rain['Dia'] = df_rain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2)+str('01'))
    df_rain['Dia'] = pd.to_datetime(df_rain['Dia'])

    correlation.render(df_export, df_rain)


pages = {
    'Análises': analysis,
    'Histórico de chuva': rain_history,
    'Histórico do clima': climate_history,
    'Histórico de exportação': export_history,
    'Histórico de preço': money_history,
}

page = st.sidebar.selectbox('Selecione uma página', list(pages.keys()))

pages[page]()
