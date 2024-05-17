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

# Create map
def show_province_distribution(df,Vietnam_coord):
    st.markdown('<h4>Province Distribution</h4>', unsafe_allow_html=True)
    map = folium.Map(location=MAP_LOCATION, zoom_start=MAP_ZOOM_START)
    df_full = pd.merge(Vietnam_coord, df, on='Province')
    for lat, lon, value, name in zip(df_full['Lat'], df_full['Long'], df_full['Total cases'], df_full['Province']):
        folium.CircleMarker(
            location=[lat, lon],
            radius=value * 0.0001,
            color='red',
            fill_color='red',
            fill_opacity=0.3,
            popup=('State: ' + str(name).capitalize() + '<br>Total Cases: ' + str(value))
        ).add_to(map)
    map_html = map._repr_html_()
    st.components.v1.html(map_html, width=800, height=600)
    

# Display about information
def about():
    st.markdown('<h4>About</h4>', unsafe_allow_html=True)
    st.write('This application provides a visualization of the COVID-19 situation in Vietnam. It displays a map showing the province-wise distribution of COVID-19 cases. It also shows bar charts representing the top 10 provinces with the highest number of active cases and the percentage distribution of active cases across provinces. It provides news updates on the latest COVID-19 news in Vietnam.')
    st.write('Please note that this application is not meant for providing real-time data and might not reflect the most recent situation in Vietnam. For the latest and most accurate information, please refer to reliable sources such as the World Health Organization (WHO), Vietnam\'s Ministry of Health, or local government agencies.')

# Tổng ca nhiễm theo tỉnh
def total_cases_by_province(df):
    df.sort_values(['Total cases'], ascending = False, inplace = True)
    fig = px.bar(df, x='Province', y='Total cases', title='Tổng ca nhiễm theo tỉnh')
    st.plotly_chart(fig)
    st.write('From the data, the total number of infected cases up to now is quite high and is continuing to increase. '
         "The highest number of infections belongs to <span style='color: blue; font-weight: bold;'>Ho Chi Minh City with more than 629,000 cases</span>, and "
         "<span style='color: blue; font-weight: bold;'>Hanoi with more than 1,646,000 cases</span>. Both cities recorded a significant number of infections.")
    
# Số ca nhiễm mới của mỗi tỉnh
def new_cases(df):
    fig = px.line(df, x='Province', y='New Cases', title='Số ca nhiễm mới của mỗi tỉnh')
    st.plotly_chart(fig)
    st.write("Number of new infections: From the data in the chart above, it shows that there is still an increase in the number of new cases although not all provinces/cities have recorded new cases recently. "
         "The province/city with the highest number of new infections is <span style='color: red; font-weight: bold;'>Dien Bien recorded 26 new cases</span>, "
         "<span style='color: red; font-weight: bold;'>Quang Binh recorded 13 new cases</span>, and "
         "<span style='color: red; font-weight: bold;'>Hai Phong recorded 11 new cases</span>. "
         "However, there are also some provinces/cities that did not record new infections during this time.", unsafe_allow_html=True)

# Tỉ lệ số ca tử vong theo tỉnh
def mortality_rate(df):
    df['Mortality Rate'] = (df['Death'] / df['Total cases']) * 100
    df_rate = df[(df['Total cases'] > 0) & (df['Death'] > 0)]
    fig_mortality_rate = px.pie(df_rate, values='Death', names='Province', title='Tỷ lệ tử vong theo tỉnh', labels={'Province': 'Province', 'Death': 'Number of Deaths'})
    fig_mortality_rate.update_traces(textposition='inside', textinfo='percent+label', insidetextorientation='radial')
    st.plotly_chart(fig_mortality_rate)
    st.write("The provinces/cities with the highest death rate are Ho Chi Minh (46.9%), followed by Binh Duong (8.26%) and Dong Nai (4.46%). Other provinces/cities also recorded a number of deaths, however, this number is lower than the above mentioned locations.")

# Mối liên hệ giữa số ca nhiễm và số ca tử vong
def plot_heatmap(df):
    fig = px.density_heatmap(df, x='Total cases', y='Death', title='Mối liên hệ giữa số ca nhiễm và số ca tử vong')
    st.plotly_chart(fig)


def vietnam():
    # Load data
    Vietnam_coord = pd.read_csv('./covid_19/data_vn/Vietnam_province_info.csv')
    data_vietnam = pd.read_csv('./covid_19/data_vn/cases_in_Vietnam.csv')
    df = data_vietnam.copy()
    df_full = pd.merge(Vietnam_coord, df, on='Province')
    
    st.title('Analyzing the COVID-19 in Vietnam')
    
    # Display dataset
    display_dataset(df_full)
    
    # Calculate total number of confirmed cases
    total_cases = df['Total cases'].sum()
    st.write('Total number of confirmed COVID 19 cases across Vietnam till date (April 12, 2024):',total_cases)
    
     # Hiển thị các biểu đồ
    total_cases_by_province(df_full)
    new_cases(df_full)
    mortality_rate(df_full)
    plot_heatmap(df_full)
    
    st.write("Based on the above data analysis, it can be seen that Vietnam is continuing to face challenges from the COVID-19 epidemic. The government has imposed restrictions and control measures to reduce the spread of the virus. However, the continued increase in cases and deaths requires continued focus and efforts on the part of governments and communities.")
    
    # Create map province_distribution
    show_province_distribution(df,Vietnam_coord)
    
    about()



# Tập dữ liệu cũ 
# Calculate total cases and active cases
# df['Total cases'] = df['Total Confirmed Cases (Viet Nam National)'] + df['Total Confirmed Cases (Foreign National)']
# df['Total Active'] = df['Total cases'] - (df['Deaths'] + df['Recovered'])

# def Confirmed_Recovered_figures(df):
#     st.markdown('<h4>Confirmed vs Recovered figures</h4>', unsafe_allow_html=True)
#     data = df[['Province', 'Total cases', 'Recovered', 'Deaths']]
#     data.sort_values('Total cases', ascending=False, inplace=True)
#     f, ax = plt.subplots(figsize=(12, 15))
#     #vẽ hai biểu đồ cột
#     sns.set_color_codes("pastel")
#     sns.barplot(x="Total cases", y="Province", data=data, label="Total", color="r")
#     sns.set_color_codes("muted")
#     sns.barplot(x="Recovered", y="Province", data=data, label="Recovered", color="g")
#     ax.legend(ncol=2, loc="lower right", frameon=True)
#     ax.set(xlim=(0, 250), ylabel="", xlabel="Cases")
#     sns.despine(left=True, bottom=True)
#     st.pyplot(f)
    
    
# # Number of foregin nationals infected in Vietnam
# def foregin_national_cases(df):
#     st.markdown('<h4>Number of foregin nationals infected in Vietnam</h4>', unsafe_allow_html=True)
#     vn_national = df['Total Confirmed Cases (Viet Nam National)'].sum()
#     foregin_national = df['Total Confirmed Cases (Foreign National)'].sum()
#     df1 = [vn_national, foregin_national]
#     labels = ['Vietnamese nationality','Foreign Nationals']
#     fig, ax = plt.subplots(figsize = (8,8))
#     # ax.pie(df1, labels=labels, startangle=90)
#     wedges, _ , autotexts = ax.pie(df1, labels=labels, startangle=90, autopct='%1.1f%%', textprops=dict(color="w"))
#     plt.setp(autotexts, size=10, weight="bold")
#     ax.axis('equal') 
#     # Add custom legend for each wedge
#     for i, autotext in enumerate(autotexts):
#         autotext.set_text(f'{labels[i]}: {df1[i]}')
#     st.pyplot(fig)

