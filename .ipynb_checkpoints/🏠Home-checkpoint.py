import streamlit as st
import pandas as pd
# ➢ st.set_page_config(
    # page_title=None, 
    # page_icon=None, 
    # layout="centered",
    #initial_sidebar_state="auto", 
    # menu_items=None
#)

# Sidebar navigation
st.set_page_config(
    page_title = "Home",
    page_icon="🏠"
)


st.title("Covid-19 outbreak prediction model")

st.write("""
This project will research and analyze data about coronavirus (COVID-19) in Vietnam and around the world.

Data is collected from the website: https://data.opendevelopmentmekong.net/dataset/coronavirus-covid-19-cases-in-vietnam/resource/d2967df9-3ef2-4d86-ad21-c14becf043fc         
""")

st.subheader("Dataset")

# Đọc file CSV
data = pd.read_csv('covid_19/data_vn/covid19-provinces_vn.csv')

# Hiển thị DataFrame trên Streamlit
st.dataframe(data)

