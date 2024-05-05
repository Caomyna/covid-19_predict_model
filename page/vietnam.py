import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium import plugins

# Constants
FIG_SIZE = (10, 12)
MAP_ZOOM_START = 5
MAP_LOCATION = [14.0583, 108.2772]

# Function to display dataset
def display_dataset(df):
    st.markdown('<h4>Dataset</h4>', unsafe_allow_html=True)
    data = df.style.background_gradient()  
    st.dataframe(data, width=2000)

# Function to create bar chart
def create_bar_chart(df, x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    sns.barplot(x=x, y=y, data=df, palette='viridis')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    st.pyplot(fig)

# Function to create pie chart
def create_pie_chart(df, labels, title):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df, labels=labels, startangle=90)
    st.pyplot(fig)

# Load data
Vietnam_coord = pd.read_csv('./covid_19/data_vn/Vietnam_province_info.csv')
data_vietnam = pd.read_csv('./covid_19/data_vn/covid19-provinces_vn.csv')
df = data_vietnam.copy()
df = df.drop(['HASC', 'ISO', 'FIPS', 'Administration Code'], axis=1)

df_full = pd.merge(Vietnam_coord, df, on='Province')

# Calculate total cases and active cases
df['Total cases'] = df['Total Confirmed Cases (Viet Nam National)'] + df['Total Confirmed Cases (Foreign National)']
df['Total Active'] = df['Total cases'] - (df['Deaths'] + df['Recovered'])


# Create map
def show_province_distribution(df):
    st.markdown('<h4>Province Distribution</h4>', unsafe_allow_html=True)
    map = folium.Map(location=MAP_LOCATION, zoom_start=MAP_ZOOM_START)
    df_full = pd.merge(Vietnam_coord, df, on='Province')
    for lat, lon, value, name in zip(df_full['Lat'], df_full['Long'], df_full['Total cases'], df_full['Province']):
        folium.CircleMarker(
            location=[lat, lon],
            radius=value * 0.01,
            color='red',
            fill_color='red',
            fill_opacity=0.3,
            popup=('State: ' + str(name).capitalize() + '<br>Total Cases: ' + str(value))
        ).add_to(map)
    map_html = map._repr_html_()
    st.components.v1.html(map_html, width=800, height=600)
    
    
def Confirmed_Recovered_figures():
    st.markdown('<h4>Confirmed vs Recovered figures</h4>', unsafe_allow_html=True)
    data = df[['Province', 'Total cases', 'Recovered', 'Deaths']]
    data.sort_values('Total cases', ascending=False, inplace=True)
    f, ax = plt.subplots(figsize=(12, 15))
    #vẽ hai biểu đồ cột
    sns.set_color_codes("pastel")
    sns.barplot(x="Total cases", y="Province", data=data, label="Total", color="r")
    sns.set_color_codes("muted")
    sns.barplot(x="Recovered", y="Province", data=data, label="Recovered", color="g")
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 250), ylabel="", xlabel="Cases")
    sns.despine(left=True, bottom=True)
    st.pyplot(f)
    
    
# Number of foregin nationals infected in Vietnam
def foregin_national_cases():
    st.markdown('<h4>Number of foregin nationals infected in Vietnam</h4>', unsafe_allow_html=True)
    vn_national = df['Total Confirmed Cases (Viet Nam National)'].sum()
    foregin_national = df['Total Confirmed Cases (Foreign National)'].sum()
    df1 = [vn_national, foregin_national]
    labels = ['Vietnamese nationality','Foreign Nationals']
    fig, ax = plt.subplots(figsize = (8,8))
    # ax.pie(df1, labels=labels, startangle=90)
    wedges, _ , autotexts = ax.pie(df1, labels=labels, startangle=90, autopct='%1.1f%%', textprops=dict(color="w"))
    plt.setp(autotexts, size=10, weight="bold")
    ax.axis('equal') 
    # Add custom legend for each wedge
    for i, autotext in enumerate(autotexts):
        autotext.set_text(f'{labels[i]}: {df1[i]}')
    st.pyplot(fig)

# Display about information
def about():
    st.markdown('<h4>About</h4>', unsafe_allow_html=True)
    st.write('This application provides a visualization of the COVID-19 situation in Vietnam. It displays a map showing the province-wise distribution of COVID-19 cases. It also shows bar charts representing the top 10 provinces with the highest number of active cases and the percentage distribution of active cases across provinces. It provides news updates on the latest COVID-19 news in Vietnam.')
    st.write('Please note that this application is not meant for providing real-time data and might not reflect the most recent situation in Vietnam. For the latest and most accurate information, please refer to reliable sources such as the World Health Organization (WHO), Vietnam\'s Ministry of Health, or local government agencies.')


# Display disclaimer
def disclaimer():
    st.markdown('<h4>Disclaimer</h4>', unsafe_allow_html=True)
    st.write('This application is provided for informational purposes only. The developer of this application is not responsible for any errors or inaccuracies in the data or any damage or loss caused by the use of this application.')



def vietnam():
    st.title('COVID-19 in Vietnam')
    
    # Display dataset
    display_dataset(df)
    
    # Calculate total number of confirmed cases
    total_cases = df['Total cases'].sum()
    st.write('Total number of confirmed COVID 19 cases across Vietnam till date (August 9, 2021):',total_cases)

    # Calculate total number of active cases
    total_active = df['Total Active'].sum()
    st.write('Total number of active COVID 2019 cases across Vietnam: ', total_active)

    # Create bar chart for top 10 provinces with highest number of active cases
    tot_cases = df.groupby('Province')['Total Active'].sum().sort_values(ascending=False).to_frame()
    top10_cases = tot_cases.head(10)
    create_bar_chart(top10_cases, 'Total Active', top10_cases.index, 'Top 10 Provinces with the Highest Number of Active COVID-19 Cases', 'Total Active Cases', 'Province')
    
    # Create map province_distribution
    show_province_distribution(df)
    
    Confirmed_Recovered_figures()

    foregin_national_cases()

    about()
    
    disclaimer()