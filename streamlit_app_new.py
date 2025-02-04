import streamlit as st
from textwrap import shorten

# Функции обработки текста (заглушки, замените на реальные)
def process_nlp(text: str) -> str:
    return f"[NLP Analysis]: {text[:150]}..."

def summarize(text: str) -> str:
    return shorten(text, width=250, placeholder="...")

# Интерфейс
st.set_page_config(page_title="HSE Legal NLP", layout="wide")

# Установка белого фона, черного текста и стилизация кнопок
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: white !important;
            color: black !important;
        }
        .stTextInput, .stTextArea {
            color: black !important;
        }
        div.stButton > button {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #0056b3 !important;
        }
        div.stAlert {
            color: black !important;
        }
        .stAlert p {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 HSE Legal NLP Platform")

# Выбор режима работы
mode = st.sidebar.selectbox("Выберите действие", ["NLP-анализ", "Суммаризация", "О проекте"])

if mode == "О проекте":
    st.header("О проекте")
    
    st.subheader("Разработчики :green[***Кайтуев Абдулла***], :green[***Шарипова Елена***], :green[***Ларичева Алина***]")

    st.subheader("[GitHub](https://github.com/persikaleshka/truth_of_the_matter)")

else:
    st.header("Введите текст")
    user_input = st.text_area("Введите текст для обработки", height=200)
    process_button = st.button("🔍 Анализировать" if mode == "NLP-анализ" else "✂️ Суммаризировать")
    
    if process_button and user_input.strip():
        with st.spinner("Обрабатываем..."):
            result = process_nlp(user_input) if mode == "NLP-анализ" else summarize(user_input)
            st.subheader("📌 Результат")
            st.success(result)
    elif process_button:
        st.warning("⚠️ Введите текст перед обработкой!")
