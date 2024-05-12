import streamlit as st
from streamlit_option_menu import option_menu
from page.home import home
from page.vietnam import vietnam
from page.world import world
from page.prediction import prediction

# Điều hướng trang
def main():
    with st.sidebar:
        choice = option_menu(
            menu_title = "Main Menu",
            options=["🏠 Trang chủ", '📈 Phân tích COVID-19 Việt Nam', '🌎 Phân tích COVID-19 Thế giới', '📊 Dự đoán'],
        )

    if choice == '🏠 Trang chủ':
        home()
    elif choice == '📈 Phân tích COVID-19 Việt Nam':
        vietnam()
    elif choice == '🌎 Phân tích COVID-19 Thế giới':
        world()
    elif choice == '📊 Dự đoán':
        prediction()
# Điều hướng trang
# def main():
#     st.sidebar.title('Menu')
#     st.sidebar.divider()
#     # Tạo menu điều hướng trang
#     menu = [
#         '🏠Trang chủ', 
#         '📈Phân tích COVID-19 Việt Nam', 
#         '🌎Phân tích COVID-19 Thế giới', 
#         '📊Dự đoán'
#     ]
#     choice = st.sidebar.radio('', menu)

#     if choice == '🏠Trang chủ':
#         home()
#     elif choice == '📈Phân tích COVID-19 Việt Nam':
#         vietnam()
#     elif choice == '🌎Phân tích COVID-19 Thế giới':
#         world()
#     elif choice == '📊Dự đoán':
#         prediction()

if __name__ == '__main__':
    main()