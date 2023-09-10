import pandas as pd
import streamlit as st
import plotly.express as px


df_export = pd.read_csv('dataset_export_soybean.csv')[['state','kg','date']]
df_export = df_export.sort_values(by=['date']).reset_index(drop=True)
df_export['Dia'] = pd.to_datetime(df_export['date'])
df_export['Mes'] = df_export['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_export['Ano'] = df_export['Dia'].apply(lambda x: str(x.year))

df_rain = pd.read_csv('dataset_precipitation_soybean.csv')[['state','date','precipitation']]
df_rain['precipitation'] = df_rain['precipitation'].str.replace(',','.').astype(float)
df_rain['Dia'] = pd.to_datetime(df_rain['date'])
df_rain['Mes'] = df_rain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_rain['Ano'] = df_rain['Dia'].apply(lambda x: str(x.year))

df_climate = pd.read_csv('temperature_brazil.csv')[['TempBulboSeco','TempBulboUmido','TempMaxima','TempMinima','UmidadeRelativa','date']]
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

df_money = pd.read_csv('dataset_prices_soybean.csv')[['date','real','usd']]
df_money['Dia'] = pd.to_datetime(df_money['date'])
df_money['Mes'] = df_money['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_money['Ano'] = df_money['Dia'].apply(lambda x: str(x.year))

df_money['real'] = df_money['real'].str.replace(',','.').astype(float)
df_money['usd'] = df_money['usd'].str.replace(',','.').astype(float)


def history_exportation():
    with st.container(): 
        st.header("Quantidade de Soja Exportada")
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)
        group_slct = st.radio("Agrupado por", ('Estados', 'Nenhum'), horizontal=True)
        
        if group_slct == 'Estados':
            options_slct = st.radio("Selecionar por", ('Top 10', 'Selecionar manualmente'), horizontal=True)
            
            df_filtred = df_export.groupby(['state',temporal_slct])['kg'].sum().reset_index()
            
            if options_slct == 'Top 10':
                df_grouped = df_export.groupby(['state'])['kg'].sum().reset_index()
                df_grouped = df_grouped.sort_values(by=['kg'], ascending=False).reset_index(drop=True)
                df_grouped = df_grouped.head(n=10)

                df_filtred = df_filtred.loc[df_filtred['state'].isin(df_grouped['state'].unique())]

            else:
                states_slct = st.multiselect('Selecione os Estados:', df_filtred['state'].unique())
                df_filtred = df_filtred.loc[df_filtred['state'].isin(states_slct)]

            graf = px.line(
                df_filtred,
                x=temporal_slct,
                y='kg',
                color='state',
            )
            graf.update_layout(
                title_text=f"Quantidade de Toneladas por Estado agrupado por {temporal_slct}",
                xaxis_title='Data',
                yaxis_title='Toneladas'
            )

            st.plotly_chart(graf, use_container_width=True)

        else:
            df_filtred = df_export.groupby([temporal_slct])['kg'].sum().reset_index()

            graf = px.line(
                df_filtred,
                x=temporal_slct,
                y='kg',
            )
            graf.update_layout(
                title_text=f"Quantidade de Toneladas por Estado agrupado por {temporal_slct}",
                xaxis_title='Data',
                yaxis_title='Toneladas'
            )

            st.plotly_chart(graf, use_container_width=True)


def history_rain():
    with st.container(): 
        st.header("Quantidade de Chuva")
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)
        group_slct = st.radio("Agrupado por", ('Estados', 'Nenhum'), horizontal=True)
        
        if group_slct == 'Estados':
            options_slct = st.radio("Selecionar por", ('Top 10', 'Selecionar manualmente'), horizontal=True)
            
            df_filtred = df_rain.groupby(['state',temporal_slct])['precipitation'].mean().round().reset_index()
            
            if options_slct == 'Top 10':
                df_grouped = df_rain.groupby(['state'])['precipitation'].mean().round().reset_index()
                df_grouped = df_grouped.sort_values(by=['precipitation'], ascending=False).reset_index(drop=True)
                df_grouped = df_grouped.head(n=10)

                df_filtred = df_filtred.loc[df_filtred['state'].isin(df_grouped['state'].unique())]

            else:
                states_slct = st.multiselect('Selecione os Estados:', df_filtred['state'].unique())
                df_filtred = df_filtred.loc[df_filtred['state'].isin(states_slct)]

            graf = px.line(
                df_filtred,
                x=temporal_slct,
                y='precipitation',
                color='state',
            )
            graf.update_layout(
                title_text=f"Quantidade de Chuva por Estado agrupado por {temporal_slct}",
                xaxis_title='Data',
                yaxis_title='Preciptação (mm)'
            )

            st.plotly_chart(graf, use_container_width=True)

        else:
            df_filtred = df_rain.groupby([temporal_slct])['precipitation'].mean().round().reset_index()

            graf = px.line(
                df_filtred,
                x=temporal_slct,
                y='precipitation',
            )
            graf.update_layout(
                title_text=f"Quantidade de Chuva por Estado agrupado por {temporal_slct}",
                xaxis_title='Data',
                yaxis_title='Preciptação (mm)'
            )

            st.plotly_chart(graf, use_container_width=True)


def history_temperatura():
    with st.container(): 
        st.header("Histórico de Clima no Brasil")
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)  
    
        df_filtred = df_climate.groupby([temporal_slct])[['Temperature','TempMaxima','TempMinima','UmidadeRelativa']].mean().round().reset_index()

        graf_temperature = px.line(
            df_filtred,
            x=temporal_slct,
            y=['Temperature','TempMaxima','TempMinima'],
        )
        graf_temperature.update_layout(
            title_text=f"Histórico de Temperatura agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='Temperatura (ºC)'
        )

        graf_humidity = px.line(
            df_filtred,
            x=temporal_slct,
            y=['UmidadeRelativa'],
        )
        graf_humidity.update_layout(
            title_text=f"Histórico de Umidade agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='Umidade (%)'
        )

        st.plotly_chart(graf_temperature, use_container_width=True)
        st.plotly_chart(graf_humidity, use_container_width=True)


def history_price():
    with st.container(): 
        st.header("Histórico do preço de soja")
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)  
    
        df_filtred = df_money.groupby([temporal_slct])[['real','usd']].mean().round().reset_index()

        graf = px.line(
            df_filtred,
            x=temporal_slct,
            y=['real','usd'],
        )
        graf.update_layout(
            title_text=f"Histórico do preço de soja agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='Valor'
        )


        st.plotly_chart(graf, use_container_width=True)


def analise():
    df_export = pd.read_csv('dataset_export_soybean.csv')[['state','kg','date']]
    df_export = df_export.sort_values(by=['date']).reset_index(drop=True)
    df_export['Dia'] = pd.to_datetime(df_export['date'])
    df_export['Mes'] = df_export['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_export['Ano'] = df_export['Dia'].apply(lambda x: str(x.year))
    df_export = df_export.loc[~df_export['state'].isin(['RO', 'MS', 'ND'])]


    df_rain = pd.read_csv('dataset_precipitation_soybean.csv')[['state','date','precipitation']]
    df_rain['precipitation'] = df_rain['precipitation'].str.replace(',','.').astype(float)
    df_rain['Dia'] = pd.to_datetime(df_rain['date'])
    df_rain['Mes'] = df_rain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
    df_rain['Ano'] = df_rain['Dia'].apply(lambda x: str(x.year))
    df_rain['Dia'] = df_rain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2)+str('01'))
    df_rain['Dia'] = pd.to_datetime(df_rain['Dia'])

    st.header("Correlação entre a quantidade exportada e preciptação")
    with st.container():
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)
        group_slct = st.radio("Agrupado por", ('Estados', 'Nenhum'), horizontal=True)
        
        if group_slct == 'Estados':
            options_slct = st.radio("Selecionar por", ('Top 10 maiores exportadores', 'Selecionar manualmente'), horizontal=True)
            
            df_filtred_export = df_export.groupby(['state',temporal_slct])['kg'].sum().reset_index()
            df_filtred_rain = df_rain.groupby(['state',temporal_slct])['precipitation'].mean().round().reset_index()
            
            if options_slct == 'Top 10 maiores exportadores':
                df_grouped = df_export.groupby(['state'])['kg'].sum().reset_index()
                df_grouped = df_grouped.sort_values(by=['kg'], ascending=False).reset_index(drop=True)
                df_grouped = df_grouped.head(n=10)
                df_filtred_export = df_filtred_export.loc[df_filtred_export['state'].isin(df_grouped['state'].unique())]
                df_filtred_rain = df_filtred_rain.loc[df_filtred_rain['state'].isin(df_grouped['state'].unique())]

            else:
                states_slct = st.multiselect('Selecione os Estados:', df_filtred_export['state'].unique())
                df_filtred_export = df_filtred_export.loc[df_filtred_export['state'].isin(states_slct)]
                df_filtred_rain = df_filtred_rain.loc[df_filtred_rain['state'].isin(states_slct)]

            df_merged = df_filtred_rain[['state','precipitation',temporal_slct]].merge(df_filtred_export[['state','kg',temporal_slct]],
                                                                                       how='inner', on=['state',temporal_slct])
            
            graf = px.scatter(
                df_merged,
                x='precipitation', 
                y='kg',
                color='state'
            )
        
        else:
            df_filtred_rain = df_rain.groupby([temporal_slct])['precipitation'].mean().round().reset_index()
            df_filtred_export = df_export.groupby([temporal_slct])['kg'].sum().reset_index()

            df_merged = df_filtred_rain[['precipitation',temporal_slct]].merge(df_filtred_export[['kg',temporal_slct]],
                                                                            how='inner', on=[temporal_slct])

            graf = px.scatter(
                df_merged,
                x='precipitation', 
                y='kg',
            )

        graf.update_layout(
            title_text=f"Quantidade de Chuva por Estado agrupado por {temporal_slct}",
            xaxis_title='Preciptação (mm)',
            yaxis_title='Quantidade de soja exportada em toneladas'
        )

        st.plotly_chart(graf, use_container_width=True)
    

pages = {
    'Análises': analise,
    'Histórico de preço': history_price,
    'Histórico de exportação': history_exportation,
    'Histórico de chuva': history_rain,
    'Histórico de temperatura': history_temperatura,
}

page = st.sidebar.selectbox('Selecione uma página', list(pages.keys()))

pages[page]()
