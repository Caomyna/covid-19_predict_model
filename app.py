import streamlit as st
from streamlit_option_menu import option_menu
from page.home import home
from page.vietnam import vietnam
from page.world import world
from page.prediction import prediction
from page.predict import predict

# Điều hướng trang
def main():
    with st.sidebar:
        choice = option_menu(
            menu_title = "Main Menu",
            options=["🏠 Home", '📈 Analysing the present COVID-19 in Vietnam', '🌎 COVID-19 Worldwide', '📊 Prediction Model'],
        )

    if choice == '🏠 Home':
        home()
    elif choice == '📈 Analysing the present COVID-19 in Vietnam':
        vietnam()
    elif choice == '🌎 COVID-19 Worldwide':
        world()
    elif choice == '📊 Prediction Model':
        predict()

if __name__ == '__main__':
    main()