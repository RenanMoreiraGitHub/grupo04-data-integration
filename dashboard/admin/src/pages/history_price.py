import streamlit as st
import plotly.express as px


def render(df_money):
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