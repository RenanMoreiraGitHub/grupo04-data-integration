import cv2
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def slice(path_img:str, path_save:str) -> None:
    img = plt.imread(path_img)[58:-55, 192:-98]
    plt.imsave(path_save, img)


def calc_percentage(img_path:str) -> float:
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    st.image(gray)

    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    st.image(thresh)
    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 3)
    st.image(opening)

    sure_bg = cv2.dilate(opening,kernel,iterations = 4)
    st.image(sure_bg)

    percentage = (np.count_nonzero(sure_bg == 0) * 100)/(sure_bg.shape[0] * sure_bg.shape[1])
    return round(percentage, 2)


def render(df_export, df_rain):
    st.header("Correlação entre a quantidade exportada e precipitação")
    with st.container():
        temporal_slct = st.radio("Visão por", ('Dia', 'Mes', 'Ano'), horizontal=True)
        group_slct = st.radio("Agrupado por", ('Estados', 'Nenhum'), horizontal=True)
        scope = st.radio("Escopo", ('trace', 'overall'), horizontal=True)
        
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
                color='state',
                trendline="ols",
                trendline_scope=scope
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
                trendline="ols"
            )

        graf.update_layout(
            title_text=f"Quantidade de Chuva por Estado agrupado por {temporal_slct}",
            xaxis_title='Precipitação (mm)',
            yaxis_title='Quantidade de soja exportada em toneladas'
        )

        st.plotly_chart(graf, use_container_width=True)
    
    st.header("Exemplo do processo de Cálculo de porcentagem de núvens na região")
    with st.container():
        uploaded_file = st.file_uploader("Upload Imagem", type=['png', 'jpg','jpeg'])
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            img_array = np.array(img)
            
            plt.imsave(r'datasets\data_raw\img.png', img_array)
            st.image(img)
            
            slice(r'datasets\data_raw\img.png', 
                  r'datasets\data\img.png')

            percentage = calc_percentage(r'datasets\data\img.png')
            st.text(f"Porcentagem: {percentage - 0.7}%")
            