import streamlit as st
import plotly.express as px


def render(df_anemometro, df_bmp, df_dht, df_npk, df_tcrt, df_umigrain):
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
            yaxis_title='mg/Kg'
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