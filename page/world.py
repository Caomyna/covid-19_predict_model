import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

def display_global_cases(df):
    latest_data = df.groupby('Country/Region').last()
    confirmed = latest_data['Confirmed'].sum()
    deaths = latest_data['Deaths'].sum()
    recovered = latest_data['Recovered'].sum()
    
    
    formatted_number_confirmed = "{:,.0f}".format(confirmed)
    formatted_number_deaths = "{:,.0f}".format(deaths)
    formatted_number_recovered = "{:,.0f}".format(recovered)

    st.write(f"""
             <div style='text-align: center;'>
                <p style='font-size: 38px; color:gray'>Coronavirus Cases</p>
                <h2 style='font-size: 38px;'><span style='color: #666666'>{formatted_number_confirmed}</span></h2>
             </div>
             """, unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"""
                 <div style='text-align: center;'>
                    <p style='font-size: 38px;color:gray'>Deaths</p>
                    <h2 style='font-size: 38px;'><span style='color: #BF2604;'>{formatted_number_deaths}</span></h2>
                </div>
                """, unsafe_allow_html=True)
    with col2:
        st.write(f"""
                 <div style='text-align: center;'>
                    <p style='font-size: 38px;color:gray'>Recovered</p>
                    <h2 style='font-size: 38px;'><span style='color: #8ACA2B;'>{formatted_number_recovered}</span></h2>
                 </div>
                 """, unsafe_allow_html=True)
        

def plot_covid_cases(df):
    confirmed = df.groupby('Date').sum()['Confirmed'].reset_index()
    deaths = df.groupby('Date').sum()['Deaths'].reset_index()
    active = df.groupby('Date').sum()['Active'].reset_index()
    recovered = df.groupby('Date').sum()['Recovered'].reset_index()

    # Create separate charts for each category
    fig_confirmed = go.Figure(data=go.Scatter(x=confirmed['Date'], y=confirmed['Confirmed'], mode='lines', name='Confirmed', line=dict(color='blue', width=2)))
    fig_deaths = go.Figure(data=go.Scatter(x=deaths['Date'], y=deaths['Deaths'], mode='lines', name='Deaths', line=dict(color='red', width=2)))
    fig_active = go.Figure(data=go.Scatter(x=active['Date'], y=active['Active'], mode='lines', name='Active', line=dict(color='orange', width=2)))
    
    fig_confirmed.update_layout(title='Worldwide COVID-19 Confirmed Cases', xaxis_title='Date', yaxis_title='Confirmed Cases', template='plotly_white')
    fig_deaths.update_layout(title='Worldwide COVID-19 Deaths Cases', xaxis_title='Date', yaxis_title='Deaths Cases', template='plotly_white')
    fig_active.update_layout(title='Worldwide COVID-19 Active Cases', xaxis_title='Date', yaxis_title='Active Cases', template='plotly_white')
    
    st.plotly_chart(fig_confirmed, use_container_width=True)
    st.plotly_chart(fig_deaths, use_container_width=True)
    st.plotly_chart(fig_active, use_container_width=True)

def plot_countries_comparison(df):
    latest_data_per_country = df.groupby('Country/Region').last().reset_index()
    latest_data_per_country_sorted = latest_data_per_country.sort_values(by='Confirmed', ascending=False)
    top_countries_confirmed = latest_data_per_country_sorted.head(10)
    fig_confirmed = px.bar(top_countries_confirmed, x='Country/Region', y='Confirmed', title='Top 10 Countries with Highest COVID-19 Confirmed Cases',labels={'Country/Region': 'Country', 'Confirmed': 'Confirmed Cases'})
    st.plotly_chart(fig_confirmed)
    st.write("""
            The graph showing the top 10 countries with the highest COVID-19 confirmed cases
            - The United States has the highest number of confirmed cases, exceeding 100 million.
            - India has the second-highest number of confirmed cases, exceeding 40 million.
            - France, Germany, Brazil, Japan, Italy, United Kingdom, Russia, and Turkey follow in the top 10 list, with confirmed cases ranging from 40 million to 20 million.
             """)
    
# Tính tỷ lệ tử vong 
def calculate_mortality_rate(df):
    latest_data_per_country = df.groupby('Country/Region').last().reset_index()
    latest_data_per_country['Mortality Rate'] = (latest_data_per_country['Deaths'] / latest_data_per_country['Confirmed']) * 100
    # Xóa các quốc gia có số ca nhiễm hoặc số ca tử vong là 0 (để tránh việc chia cho 0)
    latest_data_per_country = latest_data_per_country[(latest_data_per_country['Confirmed'] > 0) & (latest_data_per_country['Deaths'] > 0)]
    return latest_data_per_country

def plot_top_mortality_rate(df):
    df_with_mortality_rate = calculate_mortality_rate(df)
    # Chọn top 10 quốc gia có tỷ lệ tử vong cao nhất
    top_countries_mortality_rate = df_with_mortality_rate.nlargest(10, 'Mortality Rate')
    fig_top_mortality_rate = px.pie(top_countries_mortality_rate, values='Mortality Rate', names='Country/Region',title='Top 10 Countries with Highest COVID-19 Mortality Rate')
    st.plotly_chart(fig_top_mortality_rate)
    st.write("""
             Based on the chart, it can be seen that as of April 12, 2024, the countries with the highest number of deaths due to COVID-19 are Yemen(29%), Sudan(12.7%) and Syria(8.8%), 
             These are the 3 countries with the highest death rate.
             """)
    
def plot_country_data(df):
    # Lọc dữ liệu cho nước được chọn
    st.markdown("<h3 style='font-size:20px; color:#0487D9;'>Select a country to view COVID-19 data:</h3>", unsafe_allow_html=True)
    countries = df['Country/Region'].unique().tolist()
    selected_country = st.selectbox('Select a country:', countries)
    country_data = df[df['Country/Region'] == selected_country]
    country_data = country_data.sort_values(by='Date')

    # Lấy số ca nhiễm, số ca tử vong và số ca phục hồi của lần cập nhật cuối cùng
    total_confirmed = "{:,.0f}".format(country_data['Confirmed'].iloc[-1])
    total_deaths = "{:,.0f}".format(country_data['Deaths'].iloc[-1])
    total_active = "{:,.0f}".format(country_data['Active'].iloc[-1])
    total_recovered = "{:,.0f}".format(country_data['Recovered'].iloc[-1])
    
    "{:,.0f}".format(country_data['Confirmed'].iloc[-1])

    # Hiển thị tổng số ca nhiễm, số ca tử vong và số ca phục hồi
    st.write(f"<p style='font-size:16px;'><strong>Total Confirmed Cases:</strong> <span style='color:gray;'>{total_confirmed}</span></p>", unsafe_allow_html=True)
    st.write(f"<p style='font-size:16px;'><strong>Total Deaths Cases:</strong> <span style='color:red;'>{total_deaths}</span></p>", unsafe_allow_html=True)
    st.write(f"<p style='font-size:16px;'><strong>Total Recovered Cases:</strong> <span style='color:green;'>{total_recovered}</span></p>", unsafe_allow_html=True)

    # Tạo biểu đồ đường 
    fig_confirmed = go.Figure()
    fig_confirmed.add_trace(go.Scatter(x=country_data['Date'], y=country_data['Confirmed'], mode='lines', name='Confirmed',line=dict(width=2)))
    fig_confirmed.update_layout(title=f'{selected_country} Confirmed Cases',
                                xaxis_title='Date',
                                yaxis_title='Number of Confirmed Cases')

    fig_deaths = go.Figure()
    fig_deaths.add_trace(go.Scatter(x=country_data['Date'], y=country_data['Deaths'], mode='lines', name='Deaths',line=dict(color='red', width=2)))
    fig_deaths.update_layout(title=f'{selected_country} Deaths',
                            xaxis_title='Date',
                            yaxis_title='Number of Deaths Cases')

    fig_active = go.Figure()
    fig_active.add_trace(go.Scatter(x=country_data['Date'], y=country_data['Active'], mode='lines', name='Active',line=dict(color='orange', width=2)))
    fig_active.update_layout(title=f'{selected_country} Active Cases',
                                xaxis_title='Date',
                                yaxis_title='Number of Active Cases')

    # Hiển thị biểu đồ
    st.plotly_chart(fig_confirmed)
    st.plotly_chart(fig_deaths)
    st.plotly_chart(fig_active)
    
    
    
def world():
    st.title('COVID-19 Worldwide')
    
    # Load data
    df = pd.read_csv('./covid_19/data_world/covid_19_clean_complete_1.csv')
    df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y").dt.date

    # Hiển thị tổng số ca nhiễm
    display_global_cases(df)
    
    # hiển thị biểu đồ
    plot_covid_cases(df)
    
    # So sánh số liệu của các nước
    plot_countries_comparison(df)
    
    # biểu đồ tỷ lệ tử vong 
    plot_top_mortality_rate(df)
    
    st.markdown("**Report coronavirus cases**")
    st.dataframe(df)
    
    # Hiển thị dữ liệu của một quốc gia cụ thể
    plot_country_data(df)
    
    
    
    
    
