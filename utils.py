from pathlib import Path
from urllib.parse import urlparse
import html
import streamlit as st
from config import BASE_DIR

def safe_text(value):
    return html.escape(str(value or ""))

def local_file(path_value):
    if not path_value:
        return None
    path = Path(path_value)
    if not path.is_absolute():
        path = BASE_DIR / path
    return path if path.exists() else None

def show_image(path_value, caption=None, use_container_width=True):
    path = local_file(path_value)
    if path:
        st.image(str(path), caption=caption, use_container_width=use_container_width)
    else:
        st.info("Image placeholder — upload or replace this image from the Admin Dashboard.")

def valid_http_url(url):
    if not url:
        return True
    try:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False

def get_or_create_session_token():
    import uuid
    st.session_state.setdefault("visitor_session_token", uuid.uuid4().hex)
    return st.session_state.visitor_session_token
