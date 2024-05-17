import streamlit as st
import pickle
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('./covid_19/data_world/covid_19_clean_complete_1.csv')
df['Date'] = pd.to_datetime(df['Date'])

def make_global_prediction(start_date, end_date, model_confirmed, model_deaths, model_recovered):
    future = pd.DataFrame({'ds': pd.date_range(start=start_date, end=end_date, freq='D')})
    
    confirmed_forecast = model_confirmed.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
    deaths_forecast = model_deaths.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
    recovered_forecast = model_recovered.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]

    return confirmed_forecast, deaths_forecast, recovered_forecast

def make_country_prediction(start_date, end_date, country):
    df_country = df[df['Country/Region'] == country]
    df_confirmed = df_country[['Date', 'Confirmed']]
    df_confirmed.columns = ['ds', 'y']
    df_confirmed['ds'] = pd.to_datetime(df_confirmed['ds'])
    model_confirmed = Prophet(interval_width = 0.95)
    model_confirmed.fit(df_confirmed)
    
    df_deaths = df_country[['Date', 'Deaths']]
    df_deaths.columns = ['ds', 'y']
    df_deaths['ds'] = pd.to_datetime(df_deaths['ds'])
    model_deaths = Prophet(interval_width = 0.95)
    model_deaths.fit(df_deaths)
    
    df_recovered = df_country[['Date', 'Recovered']]
    df_recovered.columns = ['ds', 'y']
    df_recovered['ds'] = pd.to_datetime(df_recovered['ds'])
    model_recovered = Prophet(interval_width = 0.95)
    model_recovered.fit(df_recovered)
    
    future = pd.DataFrame({'ds': pd.date_range(start=start_date, end=end_date, freq='D')})
    
    confirmed_forecast = model_confirmed.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
    deaths_forecast = model_deaths.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
    recovered_forecast = model_recovered.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]

    return confirmed_forecast, deaths_forecast, recovered_forecast

def plot_forecast(forecast, title):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3, label='Confidence Interval')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title(title)
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

def predict():
    st.title('COVID-19 Prediction')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
    country_options = df['Country/Region'].unique()
    country_options = np.concatenate([['World'], country_options])
    country = st.selectbox('Country', country_options)
    if country == 'World':
        with open(f'models/prophet/model_confirmed.pkl', 'rb') as f:
            model_confirmed = pickle.load(f)
        with open(f'models/prophet/model_deaths.pkl', 'rb') as f:
            model_deaths = pickle.load(f)
        with open(f'models/prophet/model_recovered.pkl', 'rb') as f:
            model_recovered = pickle.load(f)

        confirmed_forecast, deaths_forecast, recovered_forecast = make_global_prediction(start_date, end_date, model_confirmed, model_deaths, model_recovered)

    else:

        confirmed_forecast, deaths_forecast, recovered_forecast = make_country_prediction(start_date, end_date, country)

    if st.button('Predict'):
        st.write('Confirmed Cases:')
        st.write(confirmed_forecast)
        plot_forecast(confirmed_forecast, 'Confirmed Cases Forecast')

        st.write('Deaths:')
        st.write(deaths_forecast)
        plot_forecast(deaths_forecast, 'Deaths Forecast')

        st.write('Recovered:')
        st.write(recovered_forecast)
        plot_forecast(recovered_forecast, 'Recovered Forecast')
