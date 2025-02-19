import pandas as pd
from utils.database import get_alumni_db

def authenticate_user(email, user_type):
    alumni_db = get_alumni_db()
    if user_type == "Alumni" and email in alumni_db["EMAIL ID"].values:
        return "Alumni"
    elif user_type == "Admin":  
        return "Admin"
    return None
