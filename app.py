import streamlit as st
from database import init_db
from auth import initialise_auth_state

st.set_page_config(
    page_title="MIL Reality Check Bangladesh",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
initialise_auth_state()

pages = [
    st.Page("pages/1_Home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/2_Reality_Wall.py", title="Reality Wall", icon="📰"),
    st.Page("pages/3_Current_Activities.py", title="Current Activities", icon="📣"),
    st.Page("pages/4_Weekly_Archive.py", title="Weekly Archive", icon="🗂️"),
    st.Page("pages/5_MIL_Resources.py", title="MIL Resources", icon="📚"),
    st.Page("pages/6_Contact.py", title="Contact", icon="✉️"),
    st.Page("pages/7_Admin_Login.py", title="Admin Login", icon="🔐"),
    st.Page("pages/8_Admin_Dashboard.py", title="Admin Dashboard", icon="⚙️"),
]

navigation = st.navigation(pages, position="sidebar")
navigation.run()