import streamlit as st
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_session
from models import AdminUser

def initialise_auth_state():
    st.session_state.setdefault("admin_authenticated", False)
    st.session_state.setdefault("admin_username", None)

def create_admin(username: str, password: str) -> bool:
    with get_session() as db:
        if db.query(AdminUser).filter(AdminUser.username == username).first():
            return False
        db.add(AdminUser(username=username, password_hash=generate_password_hash(password)))
        db.commit()
        return True

def authenticate(username: str, password: str) -> bool:
    with get_session() as db:
        user = db.query(AdminUser).filter(
            AdminUser.username == username,
            AdminUser.is_active.is_(True)
        ).first()
        if user and check_password_hash(user.password_hash, password):
            st.session_state.admin_authenticated = True
            st.session_state.admin_username = user.username
            return True
    return False

def logout():
    st.session_state.admin_authenticated = False
    st.session_state.admin_username = None

def require_admin():
    initialise_auth_state()
    if not st.session_state.admin_authenticated:
        st.warning("Administrator login is required to access this page.")
        st.stop()

def change_password(username: str, current_password: str, new_password: str):
    with get_session() as db:
        user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if not user or not check_password_hash(user.password_hash, current_password):
            return False, "Current password is incorrect."
        if len(new_password) < 8:
            return False, "New password must contain at least 8 characters."
        user.password_hash = generate_password_hash(new_password)
        db.commit()
        return True, "Password changed successfully."

def ensure_default_admin():
    with get_session() as db:
        user = db.query(AdminUser).filter(
            AdminUser.username == "admin"
        ).first()

        if not user:
            db.add(
                AdminUser(
                    username="admin",
                    password_hash=generate_password_hash("admin123"),
                    is_active=True
                )
            )
            db.commit()
