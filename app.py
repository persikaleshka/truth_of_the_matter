import streamlit as st
from pages_for_app import page_about, page_bert, page_map

def main():
    st.sidebar.title("Навигация")
    option = st.sidebar.selectbox("Выбор страницы", ["Про наш проект", "BERT", "Интерактивные карты"])

    if option == "Про наш проект":
        page_about()
    elif option == "BERT":
        page_bert()
    elif option == "Интерактивные карты":
        page_map()

if __name__ == "__main__":
    main()
