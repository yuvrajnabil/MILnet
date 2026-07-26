import streamlit as st

def language_selector():
    return st.sidebar.selectbox("Language / ভাষা", ["English", "বাংলা"], index=0)

def page_intro(title, subtitle=""):
    st.title(title)
    if subtitle:
        st.caption(subtitle)
