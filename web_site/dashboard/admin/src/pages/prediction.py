import streamlit as st


def render(df):
    st.title('Previsão de chuva para os próxmos 7 dias:')
    df = df.to_dict()

    with st.container():
        info_1, info_2, info_3, info_4 = st.columns(4,gap='medium')
        with info_1:
            st.write(f"**{df['data'][0]}**")
            st.write('☔️' if df['prediction'][0] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][0]}**")

        with info_2:
            st.write(f"**{df['data'][1]}**")
            st.write('☔️' if df['prediction'][1] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][1]}**")

        with info_3:
            st.write(f"**{df['data'][2]}**")
            st.write('☔️' if df['prediction'][2] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][2]}**")

        with info_4:
            st.write(f"**{df['data'][3]}**")
            st.write('☔️' if df['prediction'][3] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][3]}**")

    with st.container():
        info_5, info_6, info_7, info_8 = st.columns(4,gap='medium')
        
        with info_5:
            st.write(f"**{df['data'][4]}**")
            st.write('☔️' if df['prediction'][4] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][4]}**")

        with info_6:
            st.write(f"**{df['data'][5]}**")
            st.write('☔️' if df['prediction'][5] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][5]}**")

        with info_7:
            st.write(f"**{df['data'][6]}**")
            st.write('☔️' if df['prediction'][6] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][6]}**")

        with info_8:
            st.write(f"**{df['data'][7]}**")
            st.write('☔️' if df['prediction'][7] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][7]}**")

    with st.container():
        info_9, info_10, info_11, info_12 = st.columns(4,gap='medium')
        
        with info_9:
            st.write(f"**{df['data'][8]}**")
            st.write('☔️' if df['prediction'][8] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][8]}**")

        with info_10:
            st.write(f"**{df['data'][9]}**")
            st.write('☔️' if df['prediction'][9] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][9]}**")

        with info_11:
            st.write(f"**{df['data'][10]}**")
            st.write('☔️' if df['prediction'][10] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][10]}**")

        with info_12:
            st.write(f"**{df['data'][11]}**")
            st.write('☔️' if df['prediction'][11] >= 0.1 else '🌞')
            st.write(f"**{df['prediction'][11]}**")