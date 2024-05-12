import json
import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
# ➢ st.set_page_config(
    # page_title=None, 
    # page_icon=None, 
    # layout="centered",
    #initial_sidebar_state="auto", 
    # menu_items=None
#)

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Sidebar navigation
st.set_page_config(
    page_title = "Home",
    page_icon="🏠",
)


def home():    
    st.title("Covid-19 outbreak prediction model")
    animation = load_lottiefile("./lotties/Animation1.json")
    st_lottie(
        animation,
        speed=1,
        reverse=False,
        loop=True,
        quality="medium",
        # renderer="svg",
        height=500,
        width=500,
        key=None,
    )
    
    st.subheader("Problem Statement:")
    st.write("""
    We need a strong model that predicts how the viruss could spread across different countries and regions. The goal of this task is to build a model that predicts the spread of the viruss in the future
    - Analysing the present condition in Vietnam
    - Exploring the world wide data
    - Forecasting the world wide data
    - Forecasting the world wide COVID-19 cases using Prophets
    """)

    st.subheader("Dataset")
    st.write("""
    This project will research and analyze data about coronavirus (COVID-19) in Vietnam and around the world.

    Data is collected from the website: \n
    https://data.opendevelopmentmekong.net/dataset/coronavirus-covid-19-cases-in-vietnam/resource/d2967df9-3ef2-4d86-ad21-c14becf043fc  \n       
    
    https://covid19.gov.vn/: Vietnam's data set is taken from the official information portal website of the Ministry of Health of Vietnam and provides many important information related to the COVID-19 pandemic.\n

    https://www.worldometers.info/coronavirus/: The Worldometer website provides information about the COVID-19 epidemic worldwide. This is a popular data source used to track the number of infections, deaths and recoveries from the coronavirus pandemic. The website provides detailed information about disease data from countries around the world.
    """
    )

    st.markdown("<h2 style='font-size: 24px;'>Vietnam Dataset</h2>", unsafe_allow_html=True)
    data_vn = pd.read_csv('covid_19/data_vn/cases_in_Vietnam.csv')
    st.dataframe(data_vn,width=900)
    
    st.markdown("<h2 style='font-size: 24px;'>Worldwide dataset</h2>", unsafe_allow_html=True)
    st.write('Data is from February 15, 2020 to April 12, 2024.\n Last updated: April 12, 2024')
    data_vn = pd.read_csv('covid_19/data_world/covid_19_clean_complete_1.csv')
    st.dataframe(data_vn,width=900)



