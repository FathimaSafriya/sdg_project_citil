import os
import pandas as pd

DATA_PATH = "data/"
ALUMNI_FILE = os.path.join(DATA_PATH, "alumni_data.csv")
MESSAGE_FILE = os.path.join(DATA_PATH, "messages.csv")

def get_alumni_db():
    if os.path.exists(ALUMNI_FILE):
        return pd.read_csv(ALUMNI_FILE)
    return pd.DataFrame()

def get_alumni_data(email):
    alumni_db = get_alumni_db()
    return alumni_db[alumni_db["EMAIL ID"] == email].iloc[0]

def update_alumni_profile(email, country, company, job):
    alumni_db = get_alumni_db()
    alumni_db.loc[alumni_db["EMAIL ID"] == email, ["COUNTRY OF RESIDENCE", "COMPANY NAME", "JOB TITLE"]] = [country, company, job]
    alumni_db.to_csv(ALUMNI_FILE, index=False)

def get_messages():
    if os.path.exists(MESSAGE_FILE):
        return pd.read_csv(MESSAGE_FILE)
    return pd.DataFrame()

def send_admin_message(email, message):
    alumni_db = get_alumni_db()
    alum_data = alumni_db[alumni_db["EMAIL ID"] == email].iloc[0]
    new_message = pd.DataFrame([[alum_data["NAME"], alum_data["BATCH"], alum_data["DEPARTMENT"], email, message]], columns=["NAME", "BATCH", "DEPARTMENT", "EMAIL ID", "MESSAGE"])
    new_message.to_csv(MESSAGE_FILE, mode="a", header=False, index=False)
