import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from google.cloud import firestore

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
          'https://www.googleapis.com/auth/datastore']


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
launch_browser = True
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        appflow = InstalledAppFlow.from_client_secrets_file(
            '/home/graham/Dropbox/Certificates/data_sharing_python_credentials.json', SCOPES)
        if launch_browser:
            appflow.run_local_server(port=0)
        else:
            appflow.run_oconsole()
        creds = appflow.credentials
        
    # Save the credentials for the next run
    print("Writing access token to token.json")
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

print("creds.valid=",creds.valid,", creds=",creds.to_json())



db = firestore.Client(project="osd-data-sharing", credentials=creds)

# Then query for documents
events_ref = db.collection("Events").document("3X3QdHt6In7uMcKldI1r")


for event in events_ref.get(): #.whereEquals("userId","OTRPbfavESNvgNLMY7q8DjOZhje2"):
    print(event.id, event.to_dict())
