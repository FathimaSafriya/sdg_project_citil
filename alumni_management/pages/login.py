import streamlit as st
from utils.authentication import authenticate_user

def render():
    st.sidebar.title("Alumni Management System")
    user_type = st.sidebar.radio("Login as:", ("Alumni", "Admin"))
    email = st.sidebar.text_input("Email ID")

    if st.sidebar.button("Login"):
        user_role = authenticate_user(email, user_type)
        if user_role:
            st.session_state["user"] = email
            st.session_state["role"] = user_role
            st.session_state["logged_in"] = True
            st.session_state["page"] = "dashboard"
        else:
            st.sidebar.error("Invalid credentials!")

    if st.session_state.get("logged_in"):
        if st.session_state["role"] == "Alumni":
            st.session_state["page"] = "alumni_dashboard"
        elif st.session_state["role"] == "Admin":
            st.session_state["page"] = "admin_dashboard"
