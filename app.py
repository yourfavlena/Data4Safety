import time
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
import plotly.express as px

st.title('Data4Safety')
st.write("Analysis of temporary protection decision in Europe by citizenship, age and sex.")

data = pd.read_csv('estat_migr_asytpfm_en.csv/estat_migr_asytpfm_en.csv')    

tab1, tab2 = st.tabs(["Data Cleaning 🧹", "Dashboard 📊"])

with tab1:
    st.header("Data Cleaning Steps")
    st.write("Here's our dataset that we are working with:")
    st.write(data.head())
    st.write(data.shape)
    st.write(data.describe())  
    st.write('Missing values :\n',data.isna().sum())
    st.write("In this section, we will outline the steps taken to clean and preprocess the dataset.")
    st.write("We will remove the 2 columns OBS_Flag and CONF_STATUS because most of them are missing values.\n Also we will remove the rows that contains missing values in the column 'citizen'.")
    data_cleaned = data.drop(columns=['OBS_FLAG', 'CONF_STATUS'])
    data_cleaned = data_cleaned.dropna(subset=['citizen'])
    st.write(data_cleaned.head())
    st.write("Now let's check if their is any duplicate rows in the dataset.")
    st.write("Duplicate rows :\n",data_cleaned.duplicated().sum())
    st.write("No duplicate rows found.")
    
    

with tab2:
    st.header("Dashboard Visualizations")
    st.write("In this section, we will create visualizations to analyze the temporary protection decisions in Europe.")
    
    # linear chart visualization
    df_grouped = data_cleaned.groupby('TIME_PERIOD')['OBS_VALUE'].sum().reset_index()
    start_date = data_cleaned['TIME_PERIOD'].min()
    end_date = data_cleaned['TIME_PERIOD'].max()
    st.subheader(f"Temporary Protection Decisions over time by month from {start_date} to {end_date}")
    progress_bar = st.progress(0)
    status_text = st.empty()
    chart = st.line_chart(pd.DataFrame({'OBS_VALUE': [0]}, index=[df_grouped.index[0]]))
    for i in range(1, len(df_grouped) + 1):
        status_text.text(f'Processing {i}/{len(df_grouped)}')
        chart.add_rows(df_grouped.iloc[[i - 1]][['OBS_VALUE']])
        progress_bar.progress(i / len(df_grouped))
        time.sleep(0.1)

   ###########################################################################

# Geographical visualization
    st.header("Geographical Distribution of Temporary Protection Decisions by citizenship")
    
    geo_codes = ['AD','AO','BB','BI','BT','CM','CF','CY','DO','EL','FI','GE','GW',
             'ID','IS','FKG','KR','LI','LV','MG','MR','MY','NO','PE','PT','RS',
             'SD','SM','STLS','TH','UA','UY','VU','ZW']

    data_geo = data_cleaned[data_cleaned['citizen'].isin(geo_codes)].copy()

    coords = pd.DataFrame({
        'citizen': ['AD','AO','BB','BI','BT','CM','CF','CY','DO','EL','FI','GE','GW',
                    'ID','IS','FKG','KR','LI','LV','MG','MR','MY','NO','PE','PT','RS',
                    'SD','SM','STLS','TH','UA','UY','VU','ZW'],
        'lat': [42.5462, -11.2027, 13.1939, -3.3731, 27.5142, 7.3697, 6.6111, 35.1264,
                18.7357, 39.0742, 61.9241, 42.3154, 11.8037, -0.7893, None, 35.9078,
                47.1660, 56.8796, -18.7669, 4.2105, 60.4720, -9.1900, 39.3999,
                44.0165, 15.5527, 42.5, 15.8700, 48.3794, -32.5228, -16.5782,
                -15.3767, -19.0154, None, -19.0154],  # ici FKG et STLS = None
        'lon': [1.6016, 17.8739, -59.5432, 29.9189, 90.4336, 12.3547, 20.9394, 33.4299,
                -70.1627, 21.8243, 25.7482, 43.3569, -15.1804, 113.9213, None, -19.0208,
                127.7669, 9.5554, 25.4858, 46.8691, 101.9758, 8.4689, -75.0152, -8.2245,
                21.0059, 30.2176, 12.5, 100.9925, 31.1656, -56.0917, 167.1650, 17.3067, None, 29.1549]
    })


    data_cit = data_geo.merge(coords, on='citizen', how='left')
    df_grouped = data_cit.groupby(['citizen','lat','lon']).size().reset_index(name='count')
    df_grouped['radius'] = df_grouped['count'] / 100
    df_grouped['radius_scaled'] = df_grouped['radius'] * 100


    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_grouped,
        get_position=["lon", "lat"],
        get_radius="radius",
        radius_scale=500,
        get_color=[200, 30, 0, 160],
        pickable=True,
        auto_highlight=True
    )
    view_state = pdk.ViewState(
        latitude=df_grouped['lat'].mean(),
        longitude=df_grouped['lon'].mean(),
        zoom=3,
        pitch=0
    )
    r = pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
        tooltip={"text": "{citizen}\nNumber of people (request protection): {radius_scaled}"},
    )
    st.pydeck_chart(r)

#################################################################################

    # Bar chart visualization
    data_valid = data_cleaned[(data_cleaned['geo'] != 0) & (data_cleaned['sex'] != 0)].copy()

    df_grouped = data_valid.groupby(['geo', 'sex'])['OBS_VALUE'].sum().reset_index()
    fig = px.bar(
        df_grouped,
        x='geo',
        y='OBS_VALUE',
        color='sex',
        barmode='stack',
        text='OBS_VALUE',
        title="Number of People Granted Temporary Protection by Geo and Sex"
    )
    fig.update_layout(
        xaxis_title="Geo",
        yaxis_title="Number of People",
        legend_title="Sex"
    )
    st.plotly_chart(fig, use_container_width=True)

#################################################################################
    citizenship_data = {
        'citizen': ['AD','AO','BB','BI','BT','CM','CF','CY','DO','EL','FI','GE','GW',
                    'ID','IS','FKG','KR','LI','LV','MG','MR','MY','NO','PE','PT','RS',
                    'SD','SM','STLS','TH','UA','UY','VU','ZW'],
        'country': ['Andorre', 'Angola', 'Barbade', 'Burundi', 'Bhoutan', 'Cameroun', 'République centrafricaine', 
                    'Chypre', 'République dominicaine', 'Grèce', 'Finlande', 'Géorgie', 'Guinée-Bissau',
                    'Indonésie', 'Islande', 'Inconnu', 'Corée du Sud', 'Liechtenstein', 'Lettonie', 
                    'Madagascar', 'Mauritanie', 'Malaisie', 'Norvège', 'Pérou', 'Portugal', 'Serbie', 
                    'Soudan', 'Saint-Marin', 'Inconnu', 'Thaïlande', 'Ukraine', 'Uruguay', 'Vanuatu', 'Zimbabwe'],
        'continent': ['Europe','Afrique','Amériques','Afrique','Asie','Afrique','Afrique',
                    'Europe','Amériques','Europe','Europe','Europe/Asie','Afrique',
                    'Asie','Europe','Inconnu','Asie','Europe','Europe',
                    'Afrique','Afrique','Asie','Europe','Amériques','Europe','Europe',
                    'Afrique','Europe','Inconnu','Asie','Europe','Amériques','Océanie','Afrique']
    }

    df_citizenship = pd.DataFrame(citizenship_data)
    st.header("Citizenship Codes Reference")
    st.write(df_citizenship)
    