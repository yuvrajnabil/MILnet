import streamlit as st

def confirmation_checkbox(key, label="I confirm this deletion"):
    return st.checkbox(label, key=key)
