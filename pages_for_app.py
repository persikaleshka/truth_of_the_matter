
import streamlit as st
import pandas as pd
from bert_model import process_and_display
from visualization import create_map

def page_bert():
    st.title("🔍 HSE Legal BERT Platform")
    st.header("Использование BERT модели")
    st.write("Давайте что-нибудь обработаем...")

    uploaded_file = st.file_uploader("Загрузите TXT файл с делом", type=["txt"])
    
    texts = []
    
    if uploaded_file is not None:
        texts = uploaded_file.read().decode("utf-8")
        process_and_display(texts)
    else:
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""
        user_input = st.text_area("Input:", value=st.session_state.user_input)
        st.session_state.user_input = user_input
        if user_input:
            process_and_display(user_input)

def page_map():
    st.title("🔍 HSE Legal BERT Platform")
    st.header("Отображение данных на картах")
    
    dataset1 = pd.read_csv(r"data/region_stats_named_all.csv", encoding='utf-8')
    dataset2 = pd.read_csv(r"data/region_stats_named_with_text.csv", encoding='utf-8')

    create_map(
        dataset1,
        "Viridis",
        "Все найденные дела"
    )
    create_map(
        dataset2,
        "Plasma",
        "Содержащие текст"
    )

def page_about():
    st.title("🔍 HSE Legal BERT Platform")
    st.header("О проекте")
    st.markdown(
        """
        <p style="font-family: 'Times New Roman', Times, serif; font-size: 18px;">
        Исследование уголовных дел и выявление их важных характеристик - это проект, направленный на исследование данных судебных дел, для которых создается собственное веб-приложение. Веб-приложение реализует удобную работу с fine tuning BERT-моделью, позволяющей автоматически извлечь и классифицировать ключевые сущности из текстов загружаемых судебных решений, таких как регионы, даты, суммы и другие элементы, значимые для юридического анализа.
        </p>
        """,
        unsafe_allow_html=True
    )    
    st.subheader("Работали над проектом ***Кайтуев Абдулла***, ***Шарипова Елена***, ***Ларичева Алина***")
    st.subheader("[GitHub](https://github.com/persikaleshka/truth_of_the_matter)")