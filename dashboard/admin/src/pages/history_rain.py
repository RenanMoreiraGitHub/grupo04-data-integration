import streamlit as st
import plotly.express as px


def render(df_rain):
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
                yaxis_title='Precipitação (mm)'
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
