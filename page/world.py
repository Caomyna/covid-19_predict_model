import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('./covid_19/data_world/covid_19_clean_complete.csv')

def world():
    st.title('COVID-19 Worldwide')
    st.write(df)
    sns.lineplot(x='Date', y='Confirmed', data=df)
    sns.lineplot(x='Date', y='Deaths', data=df)
    sns.lineplot(x='Date', y='Recovered', data=df)