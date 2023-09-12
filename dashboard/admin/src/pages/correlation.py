import streamlit as st
import plotly.express as px



def render(df_export, df_rain):
    st.header("Correlação entre a quantidade exportada e precipitação")
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
            xaxis_title='Precipitação (mm)',
            yaxis_title='Quantidade de soja exportada em toneladas'
        )

        st.plotly_chart(graf, use_container_width=True)
    