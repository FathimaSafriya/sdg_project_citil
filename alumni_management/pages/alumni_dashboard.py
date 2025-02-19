import streamlit as st
import pandas as pd
import os
import datetime

# Define file paths
ALUMNI_FILE = "data/alumni_data.csv"
MESSAGE_FILE = "data/messages.csv"
VACANCY_FILE = "data/vacancies.csv"
APPLICATIONS_FILE = "data/applications.csv"
EVENTS_FILE = "data/events.csv"

def render():
    # Check if user is logged in and is an alumni
    if st.session_state.get("logged_in") and st.session_state["role"] == "Alumni":
        st.title("🎓 Alumni Dashboard")

        # Load alumni data
        alumni_db = pd.read_csv(ALUMNI_FILE)
        email = st.session_state["user"]
        user_data = alumni_db[alumni_db["EMAIL ID"] == email].iloc[0]

        # Birthday Greeting
        today = datetime.date.today().strftime("%Y-%m-%d")
        birthday_msg = None
        if user_data["DATE OF BIRTH"] == today:
            birthday_msg = f"🎉 Happy Birthday, {user_data['NAME']}! Wishing you success and happiness on your special day."

        # Persistent Navigation State
        if "alumni_menu" not in st.session_state:
            st.session_state["alumni_menu"] = "College Details"

        menu = ["College Details", "Update Profile", "Chat with College", "Received Applications", "View Events", "HIRE STUDENTS"]
        choice = st.selectbox("Navigate", menu, key="alumni_menu")

        # College Details
        if choice == "College Details":
            st.write("### 🏛 College Information")
            st.write("NIRF Rating: 25\nNAAC Accreditation: A++\nPlacement Rate: 85%")

        # Update Profile
        elif choice == "Update Profile":
            st.write("### ✏ Update Your Profile")
            country = st.text_input("Country of Residence", user_data["COUNTRY OF RESIDENCE"])
            company = st.text_input("Company Name", user_data["COMPANY NAME"])
            job = st.text_input("Designation", user_data["JOB TITLE"])

            if st.button("Update Profile"):
                old_company = user_data["COMPANY NAME"]
                old_job = user_data["JOB TITLE"]

                # Update CSV
                alumni_db.loc[alumni_db["EMAIL ID"] == email, ["COUNTRY OF RESIDENCE", "COMPANY NAME", "JOB TITLE"]] = [country, company, job]
                alumni_db.to_csv(ALUMNI_FILE, index=False)

                # Congratulatory Message for New Role
                if old_company != company or old_job != job:
                    job_msg = f"🎉 Congratulations, {user_data['NAME']}, on your new role at {company}! Wishing you success."
                    new_message = pd.DataFrame([[user_data["NAME"], user_data["BATCH"], user_data["DEPARTMENT"], email, job_msg, datetime.datetime.now()]], columns=["NAME", "BATCH", "DEPARTMENT", "EMAIL ID", "MESSAGE", "TIMESTAMP"])
                    new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)

                st.success("✅ Profile Updated!")

        # Chat with College
        elif choice == "Chat with College":
            st.write("### 💬 Chat with College Admin")
            if birthday_msg:
                st.success(birthday_msg)

            messages_db = pd.read_csv(MESSAGE_FILE)
            user_messages = messages_db[messages_db["EMAIL ID"] == email]
            for _, msg in user_messages.iterrows():
                st.write(f"💬 {msg['MESSAGE']}")

            chat_message = st.text_area("Type your message...")
            if st.button("Send Message"):
                new_message = pd.DataFrame([[user_data["NAME"], user_data["BATCH"], user_data["DEPARTMENT"], email, chat_message, datetime.datetime.now()]], columns=messages_db.columns)
                new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)
                st.success("✅ Message Sent!")

        # HIRE STUDENTS
        elif choice == "HIRE STUDENTS":
            st.subheader("📢 Post Job Vacancies")
            company = st.text_input("Company Name")
            qualification = st.text_input("Qualification Required")
            skillset = st.text_area("Desired Skillset")
            role = st.text_input("Job Role")
            vacancies = st.number_input("Number of Vacancies", min_value=1, step=1)

            if st.button("Submit Hiring Request"):
                new_vacancy = pd.DataFrame([[company, qualification, skillset, role, vacancies]], 
                               columns=["COMPANY NAME", "QUALIFICATION", "SKILLSET", "ROLE", "NUMBER OF VACANCIES"])
                new_vacancy.to_csv(VACANCY_FILE, mode="a", header=False, index=False)
                st.success("✅ Hiring request submitted successfully!")

        # Received Applications
        elif choice == "Received Applications":
            st.subheader("📥 Resumes Received for Hiring")
            if os.path.exists(APPLICATIONS_FILE):
                applications_db = pd.read_csv(APPLICATIONS_FILE)
                if not applications_db.empty:
                    st.write("### 📑 List of Received Resumes")
                    for index, row in applications_db.iterrows():
                        st.write(f"📌 *Company:* {row['COMPANY NAME']}")
                        st.write(f"💼 *Role:* {row['ROLE']}")
                        resume_path = row['ATTACHED RESUME']
                        if os.path.exists(resume_path):
                            with open(resume_path, "rb") as file:
                                resume_bytes = file.read()
                            st.download_button(label="📄 Download Resume", data=resume_bytes, file_name=os.path.basename(resume_path), mime="application/pdf")
                        else:
                            st.warning("⚠ Resume file not found!")
                        st.write("---")
                else:
                    st.info("No resumes received yet.")
            else:
                st.info("No resumes received yet.")

        # View Events
        elif choice == "View Events":
            st.subheader("📆 Upcoming Events")
            if os.path.exists(EVENTS_FILE):
                events_db = pd.read_csv(EVENTS_FILE)
                if not events_db.empty:
                    for index, row in events_db.iterrows():
                        st.write(f"📌 *{row['EVENT NAME']}* - 📅 {row['EVENT DATE']}")
                        if st.button(f"Register for {row['EVENT NAME']}", key=index):
                            registration_msg = f"✅ You have successfully registered for '{row['EVENT NAME']}' on {row['EVENT DATE']}!"
                            new_message = pd.DataFrame([[user_data["NAME"], user_data["BATCH"], user_data["DEPARTMENT"], email, registration_msg, datetime.datetime.now()]], columns=messages_db.columns)
                            new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)
                            st.success(f"✅ Registered for '{row['EVENT NAME']}' successfully!")
                else:
                    st.warning("⚠ No upcoming events at the moment.")
            else:
                st.warning("⚠ No upcoming events at the moment.")
