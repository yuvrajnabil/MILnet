import streamlit as st
from database import init_db
from components.styles import inject_css
init_db()
inject_css()

from database import get_session
from models import ContactMessage
from services.site_service import get_settings

st.title("Contact Us")
s = get_settings()
c1,c2 = st.columns([2,1])
with c1:
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone number")
        organisation = st.text_input("Organisation")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        submitted = st.form_submit_button("Send message")
        if submitted:
            if not all([name.strip(), email.strip(), subject.strip(), message.strip()]):
                st.error("Name, email, subject, and message are required.")
            else:
                try:
                    with get_session() as db:
                        db.add(ContactMessage(name=name.strip(), email=email.strip(), phone=phone.strip(),
                            organisation=organisation.strip(), subject=subject.strip(), message=message.strip()))
                        db.commit()
                    st.success("Your message has been saved.")
                except Exception as exc:
                    st.error(f"Could not save your message: {exc}")
with c2:
    st.info(f"Address: {s.address or 'Office address placeholder'}")
    st.info(f"Email: {s.contact_email or 'email@example.org'}")
    st.info(f"Phone: {s.phone_number or '+880 1XXXXXXXXX'}")
    st.link_button("Map / location placeholder", "https://maps.google.com")
