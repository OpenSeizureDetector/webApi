import os
import json

def load_credentials():
    cred_path = os.environ.get("CREDENTIALS_FILE", os.path.join(os.path.dirname(__file__), "../credentials.json"))
    try:
        with open(cred_path) as f:
            creds = json.load(f)
        return creds
    except Exception:
        # Return defaults or raise as appropriate
        return {
            "db_host": "localhost",
            "db_user": "osd",
            "db_password": "",
            "db_name": "osd",
            "secret_key": "default-secret"
        }