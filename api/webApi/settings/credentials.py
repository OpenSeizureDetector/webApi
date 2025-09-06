import os
import json
import logging

logging.basicConfig(level=logging.INFO)

def load_credentials():
    logging.info("credentials.py: loading credentials")
    cred_path = os.environ.get("CREDENTIALS_FILE", os.path.join(os.path.dirname(__file__), "../credentials.json"))
    try:
        with open(cred_path) as f:
            creds = json.load(f)
        # Validate required keys
        required = ["db_host", "db_user", "db_password", "db_name", "secret_key"]
        for key in required:
            if key not in creds:
                raise KeyError(f"Missing key in credentials: {key}")
        logging.info(f"credentials.py: loaded credentials: {creds}")
        return creds
    except Exception as e:
        logging.error(f"Error loading credentials: {e}")
        # Optionally, raise to stop startup if credentials are critical
        # raise
        return {
            "db_host": "localhost",
            "db_user": "osd",
            "db_password": "",
            "db_name": "osd",
            "secret_key": "default-secret"
        }