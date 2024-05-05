import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

df = pd.read_csv('./covid_19/data_world/covid_19_clean_complete.csv')

# def make_prediction(start_date, end_date, country, model):
#     with open(f'models/{model}/model_confirmed.pkl', 'rb') as f:
#         model_confirmed = pickle.load(f)
#     with open(f'models/{model}/model_deaths.pkl', 'rb') as f:
#         model_deaths = pickle.load(f)
#     with open(f'models/{model}/model_recovered.pkl', 'rb') as f:
#         model_recovered = pickle.load(f)
#     df_country = df[df['Country/Region'] == country]
#     X = df_country[['Date']].values
#     y = df_country['Confirmed'].values
#     X_scaled = X / np.max(X)
#     y_scaled = y / np.max(y)
#     model_confirmed.fit(X_scaled, y_scaled)
#     X_forecast = np.array(pd.date_range(start=start_date, end=end_date, freq='D')).reshape(-1, 1) / np.max(X)
#     y_forecast = model_confirmed.predict(X_forecast)
#     y_forecast = y_forecast * np.max(y)
#     confirmed_forecast = y_forecast
#     X = df_country[['Date']].values
#     y = df_country['Deaths'].values
#     X_scaled = X / np.max(X)
#     y_scaled = y / np.max([y])
#     model_deaths.fit(X_scaled, y_scaled)
#     X_forecast = np.array(pd.date_range(start=start_date, end=end_date, freq='D')).reshape(-1, 1) / np.max(X)
#     y_forecast = model_deaths.predict(X_forecast)
#     y_forecast = y_forecast * np.max([y])
#     deaths_forecast = y_forecast
#     X = df_country[['Date']].values
#     y = df_country['Recovered'].values
#     X_scaled = X / np.max(X)
#     y_scaled = y / np.max([y])
#     model_recovered.fit(X_scaled, y_scaled)
#     X_forecast = np.array(pd.date_range(start=start_date, end=end_date, freq='D')).reshape(-1, 1) / np.max(X)
#     y_forecast = model_recovered.predict(X_forecast)
#     y_forecast = y_forecast * np.max([y])
#     recovered_forecast = y_forecast
#     return confirmed_forecast, deaths_forecast, recovered_forecast

import streamlit as st
import pickle
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt

df = pd.read_csv('./covid_19/data_world/covid_19_clean_complete.csv')


with open(f'models/prophet/model_confirmed.pkl', 'rb') as f:
    model_confirmed = pickle.load(f)
with open(f'models/prophet/model_deaths.pkl', 'rb') as f:
    model_deaths = pickle.load(f)
with open(f'models/prophet/model_recovered.pkl', 'rb') as f:
    model_recovered = pickle.load(f)

def make_prediction(start_date, end_date, country, model):
    if model == 'prophet':
        with open(f'models/{model}/model_confirmed.pkl', 'rb') as f:
            model_confirmed = pickle.load(f)
        with open(f'models/{model}/model_deaths.pkl', 'rb') as f:
            model_deaths = pickle.load(f)
        with open(f'models/{model}/model_recovered.pkl', 'rb') as f:
            model_recovered = pickle.load(f)
        if country == 'World':
            df_confirmed = df.groupby('Date')['Confirmed'].sum().reset_index()
            df_confirmed.columns = ['ds', 'y']
            df_deaths = df.groupby('Date')['Deaths'].sum().reset_index()
            df_deaths.columns = ['ds', 'y']
            df_recovered = df.groupby('Date')['Recovered'].sum().reset_index()
            df_recovered.columns = ['ds', 'y']
        else:
            df_country = df[df['Country/Region'] == country]
            df_confirmed = df_country[['Date', 'Confirmed']]
            df_confirmed.columns = ['ds', 'y']
            df_deaths = df_country[['Date', 'Deaths']]
            df_deaths.columns = ['ds', 'y']
            df_recovered = df_country[['Date', 'Recovered']]
            df_recovered.columns = ['ds', 'y']
        future = pd.DataFrame({'ds': pd.date_range(start=start_date, end=end_date, freq='D')})
        confirmed_forecast = model_confirmed.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
        deaths_forecast = model_deaths.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
        recovered_forecast = model_recovered.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
        return confirmed_forecast, deaths_forecast, recovered_forecast
        # df_country = df[df['Country/Region'] == country]
        # df_confirmed = df_country[['Date', 'Confirmed']]
        # df_confirmed.columns = ['ds', 'y']
        # df_deaths = df_country[['Date', 'Deaths']]
        # df_deaths.columns = ['ds', 'y']
        # df_recovered = df_country[['Date', 'Recovered']]
        # df_recovered.columns = ['ds', 'y']
        # future = pd.DataFrame({'ds': pd.date_range(start=start_date, end=end_date, freq='D')})
        # confirmed_forecast = model_confirmed.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
        # deaths_forecast = model_deaths.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
        # recovered_forecast = model_recovered.predict(future)[['ds', 'yhat','yhat_lower','yhat_upper']]
        # return confirmed_forecast, deaths_forecast, recovered_forecast
       
    elif model == 'Linear Regression':
        # Code for linear regression model
        pass
    elif model == 'SVR':
        # Code for SVR model
        pass
    
def plot_forecast_prophet(model, forecast, title):
    fig = model.plot(forecast)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.3, label='Confidence Interval')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title(title)
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

def prediction():
    st.title('COVID-19 Prediction')
    start_date = st.date_input('Start Date')
    end_date = st.date_input('End Date')
    country_options = df['Country/Region'].unique()
    country_options = np.concatenate([['World'], country_options])
    country = st.selectbox('Country', country_options)
    if country == 'World':
        country = None
    # country = st.selectbox('Country', df['Country/Region'].unique())
    model = st.selectbox('Model', ['Linear Regression', 'SVR','prophet'])
    if st.button('Predict'):
        confirmed_forecast, deaths_forecast, recovered_forecast = make_prediction(start_date, end_date, country, model)
        st.write('Confirmed Cases:')
        st.write(confirmed_forecast)
        plot_forecast_prophet(model_confirmed, confirmed_forecast, 'Confirmed Cases Forecast')
        st.write('Deaths:')
        st.write(deaths_forecast)
        plot_forecast_prophet(model_deaths, deaths_forecast, 'Deaths Forecast')
        st.write('Recovered:')
        st.write(recovered_forecast)
        plot_forecast_prophet(model_recovered, recovered_forecast, 'Recovered Forecast')