import streamlit as st
import html

def page_about():
    st.title("HSE Truth of the matter")
    st.subheader("About this coursework")

    st.subheader("Created by :green[***Kaituev Abdulla***], :green[***Sharipova Elena***], :green[***Laricheva Alina***]")

    st.subheader("[GitHub](https://github.com/persikaleshka/truth_of_the_matter)")

def page_summarize():
    st.title("HSE Truth of the matter")
    st.write("Welcome")
    st.write("Let's summarize something...")

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    user_input = st.text_area("Input:", value=st.session_state.user_input)
    st.session_state.user_input = user_input

    if user_input:
        summarized_text = user_input
        s_len = len(summarized_text)
        u_len = len(user_input)
        st.write(summarized_text)
        st.markdown("---")
        st.write(
            f"original text length - :blue[{u_len}] vs :green[{s_len}] - summarized text length")
        st.write(f"Shortened by :green[{100 * (1 - s_len / u_len)}%]")


def page_nlp():
    st.title("HSE Truth of the matter")
    st.write("Welcome")
    st.write("Let's predict something...")

    if "user_input" not in st.session_state:
        st.session_state.user_input = ""
    user_input = st.text_area("Input:", value=st.session_state.user_input)
    st.session_state.user_input = user_input

    if user_input:
        st.write("You selected NLP")

def main():
    st.set_page_config(layout='wide')
    st.sidebar.title("Navigation")

    nav_option = st.sidebar.radio("Go To", ["***NLP***", "***Summarize***", "***About***"],
                                  captions=["Classify identities in text", "Summarize large text",
                                            "About this project"], label_visibility="hidden")

    if nav_option == "***NLP***":
        page_nlp()
    elif nav_option == "***Summarize***":
        page_summarize()
    elif nav_option == "***About***":
        page_about()
    else:
        page_nlp()


if __name__ == "__main__":
    main()
