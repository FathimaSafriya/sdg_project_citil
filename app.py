import streamlit as st
import pandas as pd
import datetime
import os


ALUMNI_FILE = "alumni_data.csv"
MESSAGE_FILE = "messages.csv"
VACANCY_FILE = "vacancies.csv"
APPLICATIONS_FILE = "applications.csv"
EVENTS_FILE = "events.csv"


if os.path.exists(ALUMNI_FILE):
    alumni_db = pd.read_csv(ALUMNI_FILE)
else:
    st.error("Database file not found!")
    alumni_db = pd.DataFrame()


if not os.path.exists(MESSAGE_FILE):
    pd.DataFrame(columns=["NAME", "BATCH", "DEPARTMENT", "EMAIL ID", "MESSAGE", "TIMESTAMP"]).to_csv(MESSAGE_FILE, index=False)
messages_db = pd.read_csv(MESSAGE_FILE)


if not os.path.exists(VACANCY_FILE):
    pd.DataFrame(columns=["COMPANY NAME", "QUALIFICATION", "SKILLSET", "ROLE", "NUMBER OF VACANCIES"]).to_csv(VACANCY_FILE, index=False)


if not os.path.exists(APPLICATIONS_FILE):
    pd.DataFrame(columns=["COMPANY NAME", "QUALIFICATION", "SKILLSET", "ROLE", "NUMBER OF VACANCIES", "ATTACHED RESUME"]).to_csv(APPLICATIONS_FILE, index=False)


if not os.path.exists(EVENTS_FILE):
    pd.DataFrame(columns=["EVENT NAME", "EVENT DATE"]).to_csv(EVENTS_FILE, index=False)



def authenticate_user(email, user_type):
    if user_type == "Alumni" and email in alumni_db["EMAIL ID"].values:
        return "Alumni"
    elif user_type == "Admin":  
        return "Admin"
    return None


st.sidebar.title("Alumni Management System")
user_type = st.sidebar.radio("Login as:", ("Alumni", "Admin"))
email = st.sidebar.text_input("Email ID")

if st.sidebar.button("Login"):
    user_role = authenticate_user(email, user_type)
    if user_role:
        st.session_state["user"] = email
        st.session_state["role"] = user_role
        st.session_state["logged_in"] = True
    else:
        st.sidebar.error("Invalid credentials!")


if st.session_state.get("logged_in"):
    if st.session_state["role"] == "Alumni":
        st.title("🎓 Alumni Dashboard")
        menu = ["College Details", "Update Profile", "Chat with College", "Received Applications", "View Events", "HIRE STUDENTS"]
        choice = st.selectbox("Navigate", menu)

        
        user_data = alumni_db[alumni_db["EMAIL ID"] == email].iloc[0]

        
        today = datetime.date.today().strftime("%Y-%m-%d")
        birthday_msg = None
        if user_data["DATE OF BIRTH"] == today:
            birthday_msg = f"🎉 Happy Birthday, {user_data['NAME']}! Wishing you success and happiness on your special day."

        if choice == "College Details":
            st.write("### 🏛 College Information")
            st.write("NIRF Rating: 25\nNAAC Accreditation: A++\nPlacement Rate: 85%")

        elif choice == "Update Profile":
            st.write("### ✏ Update Your Profile")
            country = st.text_input("Country of Residence", user_data["COUNTRY OF RESIDENCE"])
            company = st.text_input("Company Name", user_data["COMPANY NAME"])
            job = st.text_input("Designation", user_data["JOB TITLE"])

            if st.button("Update Profile"):
                old_company = user_data["COMPANY NAME"]
                old_job = user_data["JOB TITLE"]

                
                alumni_db.loc[alumni_db["EMAIL ID"] == email, ["COUNTRY OF RESIDENCE", "COMPANY NAME", "JOB TITLE"]] = [country, company, job]
                alumni_db.to_csv(ALUMNI_FILE, index=False)

                
                if old_company != company or old_job != job:
                    job_msg = f"🎉 Congratulations, {user_data['NAME']}, on your new role at {company}! Wishing you success."
                    new_message = pd.DataFrame([[user_data["NAME"], user_data["BATCH"], user_data["DEPARTMENT"], email, job_msg, datetime.datetime.now()]], columns=messages_db.columns)
                    new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)

                st.success("✅ Profile Updated!")

        elif choice == "Chat with College":
            st.write("### 💬 Chat with College Admin")
            if birthday_msg:
                st.success(birthday_msg)

            user_messages = messages_db[messages_db["EMAIL ID"] == email]
            for _, msg in user_messages.iterrows():
                st.write(f"💬 {msg['MESSAGE']}")

            chat_message = st.text_area("Type your message...")
            if st.button("Send Message"):
                new_message = pd.DataFrame([[user_data["NAME"], user_data["BATCH"], user_data["DEPARTMENT"], email, chat_message, datetime.datetime.now()]], columns=messages_db.columns)
                new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)
                st.success("✅ Message Sent!")

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

                            st.download_button(
                                label="📄 Download Resume",
                                data=resume_bytes,
                                file_name=os.path.basename(resume_path),
                                mime="application/pdf"
                            )
                        else:
                            st.warning("⚠ Resume file not found!")

                        st.write("---")
                else:
                    st.info("No resumes received yet.")
            else:
                st.info("No resumes received yet.")


        
        elif choice == "View Events":
            st.subheader("📆 Upcoming Events")
    
    
            if os.path.exists(EVENTS_FILE):
                events_db = pd.read_csv(EVENTS_FILE)
                if not events_db.empty:
                    for index, row in events_db.iterrows():
                        st.write(f"📌 *{row['EVENT NAME']}* - 📅 {row['EVENT DATE']}")
                
                        if st.button(f"Register for {row['EVENT NAME']}", key=index):
                   
                           registration_msg = f"✅ You have successfully registered for '{row['EVENT NAME']}' on {row['EVENT DATE']}!"
                    
                    
                           new_message = pd.DataFrame([[user_data["NAME"], user_data["BATCH"], user_data["DEPARTMENT"], email, registration_msg, datetime.datetime.now()]], 
                                               columns=messages_db.columns)
                           new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)
                    
                           st.success(f"✅ Registered for '{row['EVENT NAME']}' successfully!")
                else:
                    st.warning("⚠ No upcoming events at the moment.")
            else:
                st.warning("⚠ No upcoming events at the moment.")






        

    elif st.session_state["role"] == "Admin":
        st.title("🛠 Admin Dashboard")
        menu = ["View Alumni Messages", "Update Events", "Chat with Alumni", "Search Alumni", "View Vacancies","Vacancy Dashboard"]
        choice = st.selectbox("Navigate", menu)

        if choice == "View Alumni Messages":
            st.write("### 📩 Messages from Alumni")
            for _, msg in messages_db.iterrows():
                st.write(f"📩 {msg['NAME']} (Batch {msg['BATCH']}, {msg['DEPARTMENT']}):")
                st.write(f"💬 {msg['MESSAGE']}")
                st.write("---")

        elif choice == "Update Events":
            st.write("### 📅 Manage Events")
            event = st.text_input("Event Name")
            date = st.date_input("Event Date")
            if st.button("Add Event"):
                new_event = pd.DataFrame([[event, date]], columns=["EVENT NAME", "EVENT DATE"])
                new_event.to_csv(EVENTS_FILE, mode="a", header=False, index=False)
                st.success(f"✅ Event '{event}' added for {date}!")

        elif choice == "Chat with Alumni":
            st.write("### 💬 Chat with Alumni")
            alumni_email = st.selectbox("Select Alumni", alumni_db["EMAIL ID"].unique())
            chat_message = st.text_area("Admin Message")
            if st.button("Send Message"):
                alum_data = alumni_db[alumni_db["EMAIL ID"] == alumni_email].iloc[0]
                admin_msg = f"📢 College Admin: {chat_message}"
                new_message = pd.DataFrame([[alum_data["NAME"], alum_data["BATCH"], alum_data["DEPARTMENT"], alumni_email, admin_msg, datetime.datetime.now()]], columns=messages_db.columns)
                new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)
                st.success("✅ Message Sent to Alumni!")
                
        elif choice == "View Vacancies":
            st.subheader("📋 Job Vacancies")

            vacancies_db = pd.read_csv(VACANCY_FILE)

            if not vacancies_db.empty:
                st.write("### 🔍 Job Openings Submitted by Alumni")
                selected_index = st.selectbox(
                    "Select a Vacancy", 
                    vacancies_db.index, 
                    format_func=lambda x: f"{vacancies_db.loc[x, 'COMPANY NAME']} - {vacancies_db.loc[x, 'ROLE']}"
                )

        # File uploader should be outside the button condition
                resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

                if resume_file and st.button("Attach Resume & Respond"):
                    try:
                # Ensure the "resumes" directory exists
                        os.makedirs("resumes", exist_ok=True)

                # Save the uploaded PDF resume
                        save_path = f"resumes/{resume_file.name}"
                        with open(save_path, "wb") as f:
                            f.write(resume_file.getbuffer())

                # Load applications.csv, or create if it doesn’t exist
                        if os.path.exists(APPLICATIONS_FILE):
                            applications_db = pd.read_csv(APPLICATIONS_FILE)
                        else:
                            applications_db = pd.DataFrame(columns=vacancies_db.columns.tolist() + ["ATTACHED RESUME"])

                # Get selected vacancy details and update resume column
                        vacancy_data = vacancies_db.loc[[selected_index]].copy()
                        vacancy_data["ATTACHED RESUME"] = save_path

                # Concatenate to add new row
                        applications_db = pd.concat([applications_db, vacancy_data], ignore_index=True)

                # Save back to CSV
                        applications_db.to_csv(APPLICATIONS_FILE, index=False)

                        st.success("✅ Resume attached and saved successfully!")
                    except Exception as e:
                        st.error(f"❌ Error saving resume: {str(e)}")

                


        
        elif choice == "Search Alumni":
            st.subheader("🔍 Search Alumni")
    
            # Load Alumni Data
            alumni_db = pd.read_csv(ALUMNI_FILE)
    
            # Search Input
            search_query = st.text_input("Enter Name, Batch, Department, or Company")
    
            # Filter Results
            if search_query:
                filtered_alumni = alumni_db[
                    alumni_db.apply(lambda row: search_query.lower() in row.astype(str).str.lower().to_list(), axis=1)
                ]
                if not filtered_alumni.empty:
                    st.write("### 🎓 Search Results")
                    st.dataframe(filtered_alumni)

                    # Resume Attachment Feature
                    selected_index = st.selectbox("Select an Alumni", filtered_alumni.index, format_func=lambda x: f"{filtered_alumni.loc[x, 'NAME']} - {filtered_alumni.loc[x, 'COMPANY NAME']}")
            
                    if st.button("Attach Resume & Respond"):
                        resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
                        if resume_file:
                            save_path = f"resumes/{resume_file.name}"
                            with open(save_path, "wb") as f:
                                f.write(resume_file.getbuffer())

                            alumni_db.loc[selected_index, "ATTACHED RESUME"] = save_path
                            alumni_db.to_csv(APPLICATIONS_FILE, mode="a", header=False, index=False)
                            st.success("✅ Resume attached and sent to alumni!")

                else:
                    st.warning("⚠ No matching alumni found.")
            else:
                st.info("🔹 Type a keyword to search alumni.")

            # Power BI Report Embed
            st.write("### 📊 Alumni Insights - Power BI Dashboard")
    
            # Replace <EMBED_URL> with the actual Power BI embed link
            POWER_BI_EMBED_URL = "https://app.powerbi.com/reportEmbed?reportId=2c79391e-8a8b-42fd-9519-df8599b4d468&autoAuth=true&ctid=085c606c-851a-4f29-9538-639c1a6f40ee"
    
            st.components.v1.iframe(POWER_BI_EMBED_URL, width=850, height=450)


        elif choice == "Vacancy Dashboard":
            st.subheader("📊 Vacancy Dashboard - Power BI")

    # Power BI Embedded Report Link
            VACANCY_POWER_BI_URL = "https://app.powerbi.com/reportEmbed?reportId=9f162f17-971e-4eff-b714-ea84b23db6f2&autoAuth=true&ctid=085c606c-851a-4f29-9538-639c1a6f40ee"

    # Embed Power BI dashboard using iframe
            st.components.v1.iframe(VACANCY_POWER_BI_URL, width=1000, height=600)

            st.info("🔹 This dashboard provides insights into job vacancies, applications, and hiring trends.")




st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())



