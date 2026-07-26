import streamlit as st
from services.site_service import get_settings

def render_footer():
    s = get_settings()
    st.markdown(
        f"""<div class="footer">
        <h3>{s.website_name}</h3>
        <p>{s.slogan}</p>
        <p>📧 {s.contact_email or 'contact@example.org'} &nbsp; | &nbsp;
        ☎ {s.phone_number or '+880 1XXXXXXXXX'} &nbsp; | &nbsp;
        📍 {s.address or 'Dhaka, Bangladesh'}</p>
        <p>Facebook · Instagram · YouTube · LinkedIn</p>
        </div>""", unsafe_allow_html=True
    )
