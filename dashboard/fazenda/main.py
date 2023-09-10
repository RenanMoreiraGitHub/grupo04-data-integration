import pandas as pd
import streamlit as st
import plotly.express as px


df_anemometro = pd.read_parquet('df_anemometro.parquet')
df_anemometro['Dia'] = pd.to_datetime(df_anemometro['data_hora'])
df_anemometro['Mes'] = df_anemometro['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_anemometro['Ano'] = df_anemometro['Dia'].apply(lambda x: str(x.year))

df_bmp = pd.read_parquet('df_bmp.parquet')
df_bmp['Dia'] = pd.to_datetime(df_bmp['data_hora'])
df_bmp['Mes'] = df_bmp['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_bmp['Ano'] = df_bmp['Dia'].apply(lambda x: str(x.year))

df_dht = pd.read_parquet('df_dht.parquet')
df_dht['Dia'] = pd.to_datetime(df_dht['data_hora'])
df_dht['Mes'] = df_dht['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_dht['Ano'] = df_dht['Dia'].apply(lambda x: str(x.year))

df_npk = pd.read_parquet('df_npk.parquet')
df_npk['Dia'] = pd.to_datetime(df_npk['data_hora'])
df_npk['Mes'] = df_npk['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_npk['Ano'] = df_npk['Dia'].apply(lambda x: str(x.year))

df_tcrt = pd.read_parquet('df_tcrt.parquet')
df_tcrt['Dia'] = pd.to_datetime(df_tcrt['data_hora'])
df_tcrt['Mes'] = df_tcrt['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_tcrt['Ano'] = df_tcrt['Dia'].apply(lambda x: str(x.year))

df_umigrain = pd.read_parquet('df_umigrain.parquet')
df_umigrain['Dia'] = pd.to_datetime(df_umigrain['data_hora'])
df_umigrain['Mes'] = df_umigrain['Dia'].apply(lambda x: str(x.year)+str(x.month).zfill(2))
df_umigrain['Ano'] = df_umigrain['Dia'].apply(lambda x: str(x.year))


def history_sensors():
    with st.container():
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)
        df_filtred_anemometro = df_anemometro.groupby([temporal_slct])[['air-speed']].mean().reset_index()        
        df_filtred_bmp = df_bmp.groupby([temporal_slct])[['temperature','pressure']].mean().reset_index()        
        df_filtred_dht = df_dht.groupby([temporal_slct])[['humidity']].mean().reset_index()        
        df_filtred_npk = df_npk.groupby([temporal_slct])[['nitrogen','phosphorus','potassium']].mean().reset_index()        
        df_filtred_tcrt = df_tcrt.groupby([temporal_slct])[['capacity','collected']].mean().reset_index()        
        df_filtred_umigrain = df_umigrain.groupby([temporal_slct])[['humidity_grain']].mean().reset_index()        

        graf_anemometro = px.line(
            df_filtred_anemometro,
            x=temporal_slct,
            y='air-speed',
        )

        graf_anemometro.update_layout(
            title_text=f"Velocidade do vento agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='km/h'
        )

        graf_bmp_temperature = px.line(
            df_filtred_bmp,
            x=temporal_slct,
            y='temperature',
        )
        graf_bmp_temperature.update_layout(
            title_text=f"Temperatura agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='ºC'
        )

        graf_bmp_pressure = px.line(
            df_filtred_bmp,
            x=temporal_slct,
            y='pressure',
        )
        graf_bmp_pressure.update_layout(
            title_text=f"Pressão atmosférica agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='atm'
        )

        graf_dht = px.line(
            df_filtred_dht,
            x=temporal_slct,
            y='humidity',
        )
        graf_dht.update_layout(
            title_text=f"Umidade agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='humidity'
        )

        graf_npk = px.line(
            df_filtred_npk,
            x=temporal_slct,
            y=['nitrogen','phosphorus','potassium'],
        )
        graf_npk.update_layout(
            title_text=f"Porcentagem de Nitrogenio, Fosforo e Potassio agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='NPK(%)'
        )

        graf_tcrt = px.line(
            df_filtred_tcrt,
            x=temporal_slct,
            y=['capacity','collected'],
        )
        graf_tcrt.update_layout(
            title_text=f"Capacidade do silo agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='Capacidade'
        )

        graf_umigrain = px.line(
            df_filtred_umigrain,
            x=temporal_slct,
            y=['humidity_grain'],
        )
        graf_umigrain.update_layout(
            title_text=f"Capacidade do silo agrupado por {temporal_slct}",
            xaxis_title='Data',
            yaxis_title='Capacidade'
        )

        st.header("Anemometro")
        st.plotly_chart(graf_anemometro, use_container_width=True) 
        st.header("BMP")
        st.plotly_chart(graf_bmp_temperature, use_container_width=True) 
        st.plotly_chart(graf_bmp_pressure, use_container_width=True) 
        st.header("DHT")
        st.plotly_chart(graf_dht, use_container_width=True) 
        st.header("NPK")
        st.plotly_chart(graf_npk, use_container_width=True)
        st.header("TCRT")
        st.plotly_chart(graf_tcrt, use_container_width=True)
        st.header("Umigrain")
        st.plotly_chart(graf_umigrain, use_container_width=True)

pages = {
    'Histórico de anemometro': history_sensors,
}

page = st.sidebar.selectbox('Selecione uma página', list(pages.keys()))

pages[page]()