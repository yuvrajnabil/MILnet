import streamlit as st
from database import init_db
from components.styles import inject_css
init_db()
inject_css()

from auth import initialise_auth_state, authenticate, logout

initialise_auth_state()
st.title("Admin Login")
if st.session_state.admin_authenticated:
    st.success(f"Logged in as {st.session_state.admin_username}")
    if st.button("Open Admin Dashboard"):
        st.switch_page("pages/8_Admin_Dashboard.py")
    if st.button("Logout"):
        logout(); st.rerun()
else:
    with st.form("admin_login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            if authenticate(username.strip(), password):
                st.success("Login successful.")
                st.switch_page("pages/8_Admin_Dashboard.py")
            else:
                st.error("Invalid username or password.")
