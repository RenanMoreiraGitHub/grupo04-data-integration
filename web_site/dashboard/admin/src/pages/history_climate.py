import streamlit as st
import plotly.express as px


def render(df_climate):
    with st.container(): 
        st.header("Histórico de Clima no Brasil")
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)  
    
        df_filtred = df_climate.groupby([temporal_slct])[['Temperature','TempMaxima',
                                                          'TempMinima','UmidadeRelativa']].mean().round().reset_index()

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

