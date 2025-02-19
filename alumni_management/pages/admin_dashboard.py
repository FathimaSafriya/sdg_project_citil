import streamlit as st
import pandas as pd
import os
import datetime

# File Paths
ALUMNI_FILE = "data/alumni_data.csv"
MESSAGE_FILE = "data/messages.csv"
VACANCY_FILE = "data/vacancies.csv"
APPLICATIONS_FILE = "data/applications.csv"
EVENTS_FILE = "data/events.csv"

# Load Databases
messages_db = pd.read_csv(MESSAGE_FILE) if os.path.exists(MESSAGE_FILE) else pd.DataFrame(columns=['NAME', 'BATCH', 'DEPARTMENT', 'EMAIL ID', 'MESSAGE', 'TIMESTAMP'])
alumni_db = pd.read_csv(ALUMNI_FILE) if os.path.exists(ALUMNI_FILE) else pd.DataFrame(columns=['NAME', 'BATCH', 'DEPARTMENT', 'EMAIL ID'])

def render():
    if 'role' in st.session_state and st.session_state['role'] == 'Admin':
        st.title('🛠 Admin Dashboard')
        menu = ['View Alumni Messages', 'Update Events', 'Chat with Alumni', 'Search Alumni', 'View Vacancies', 'Vacancy Dashboard']
        choice = st.selectbox('Navigate', menu)

        if choice == 'View Alumni Messages':
            st.write('### 📩 Messages from Alumni')
            for _, msg in messages_db.iterrows():
                st.write(f"📩 {msg['NAME']} (Batch {msg['BATCH']}, {msg['DEPARTMENT']}):")
                st.write(f"💬 {msg['MESSAGE']}")
                st.write('---')

        elif choice == 'Update Events':
            st.write('### 📅 Manage Events')
            event = st.text_input('Event Name')
            date = st.date_input('Event Date')
            if st.button('Add Event'):
                new_event = pd.DataFrame([[event, date]], columns=['EVENT NAME', 'EVENT DATE'])
                new_event.to_csv(EVENTS_FILE, mode='a', header=False, index=False)
                st.success(f"✅ Event '{event}' added for {date}!")

        elif choice == 'Chat with Alumni':
            st.write('### 💬 Chat with Alumni')
            alumni_email = st.selectbox('Select Alumni', alumni_db['EMAIL ID'].unique())
            chat_message = st.text_area('Admin Message')
            if st.button('Send Message'):
                alum_data = alumni_db[alumni_db['EMAIL ID'] == alumni_email].iloc[0]
                admin_msg = f"📢 College Admin: {chat_message}"
                new_message = pd.DataFrame([[alum_data['NAME'], alum_data['BATCH'], alum_data['DEPARTMENT'], alumni_email, admin_msg, datetime.datetime.now()]], columns=messages_db.columns)
                new_message.to_csv(MESSAGE_FILE, mode='a', header=False, index=False)
                st.success('✅ Message Sent to Alumni!')

        elif choice == 'View Vacancies':
            st.subheader('📋 Job Vacancies')
            vacancies_db = pd.read_csv(VACANCY_FILE) if os.path.exists(VACANCY_FILE) else pd.DataFrame(columns=['COMPANY NAME', 'ROLE'])

            if not vacancies_db.empty:
                st.write('### 🔍 Job Openings Submitted by Alumni')
                selected_index = st.selectbox(
                    'Select a Vacancy', 
                    vacancies_db.index, 
                    format_func=lambda x: f"{vacancies_db.loc[x, 'COMPANY NAME']} - {vacancies_db.loc[x, 'ROLE']}"
                )

                resume_file = st.file_uploader('Upload Resume (PDF)', type=['pdf'])
                if resume_file and st.button('Attach Resume & Respond'):
                    try:
                        os.makedirs('resumes', exist_ok=True)
                        save_path = f"resumes/{resume_file.name}"
                        with open(save_path, 'wb') as f:
                            f.write(resume_file.getbuffer())

                        applications_db = pd.read_csv(APPLICATIONS_FILE) if os.path.exists(APPLICATIONS_FILE) else pd.DataFrame(columns=vacancies_db.columns.tolist() + ['ATTACHED RESUME'])
                        vacancy_data = vacancies_db.loc[[selected_index]].copy()
                        vacancy_data['ATTACHED RESUME'] = save_path
                        applications_db = pd.concat([applications_db, vacancy_data], ignore_index=True)
                        applications_db.to_csv(APPLICATIONS_FILE, index=False)
                        st.success('✅ Resume attached and saved successfully!')
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