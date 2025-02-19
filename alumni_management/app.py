import streamlit as st
from pages import login, alumni_dashboard, admin_dashboard

if st.session_state.get("logged_in"):
    if st.session_state.get("role") == "Alumni":
        alumni_dashboard.render()
    elif st.session_state.get("role") == "Admin":
        admin_dashboard.render()
else:
    login.render()

st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())
