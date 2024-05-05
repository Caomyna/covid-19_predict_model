import pickle
import pandas as pd
from prophet import Prophet

# Load the preprocessed data
df = pd.read_csv('../../covid_19/data_world/covid_19_clean_complete.csv')

# start_date = ''
# end_date = ''
# future = pd.DataFrame({'ds': pd.date_range(start=start_date, end=end_date)})
# Tạo dataframe cho các ngày bạn muốn dự đoán
# future = m_confirmed.make_future_dataframe(periods=365) 

# Create a Prophet model for confirmed cases
confirmed = df.groupby('Date').sum()['Confirmed'].reset_index()
confirmed.columns = ['ds','y']
confirmed['ds'] = pd.to_datetime(confirmed['ds'])
m_confirmed = Prophet(interval_width = 0.95)
m_confirmed.fit(confirmed)

# Create a Prophet model for deaths
deaths = df.groupby('Date').sum()['Deaths'].reset_index()
deaths.columns = ['ds','y']
deaths['ds'] = pd.to_datetime(deaths['ds'])
m_deaths = Prophet(interval_width = 0.95)
m_deaths.fit(deaths)

# Create a Prophet model for recovered cases
recovered = df.groupby('Date').sum()['Recovered'].reset_index()
recovered.columns = ['ds','y']
recovered['ds'] = pd.to_datetime(recovered['ds'])
m_recovered = Prophet(interval_width = 0.95)
m_recovered.fit(recovered)

# Save the models to .plk files
with open('model_confirmed.pkl', 'wb') as f:
    pickle.dump(m_confirmed, f)

with open('model_deaths.pkl', 'wb') as f:
    pickle.dump(m_deaths, f)

with open('model_recovered.pkl', 'wb') as f:
    pickle.dump(m_recovered, f)
    