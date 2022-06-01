import firebase_admin
import firebase_admin.firestore

cred_obj = firebase_admin.credentials.Certificate('certificates/osd-data-sharing-firebase-adminsdk-nwtpa-c22d94043e.json')
default_app = firebase_admin.initialize_app(cred_obj)

#                                            , {
#	'databaseURL':databaseURL
#})

db = firebase_admin.firestore.client()
ref = db.collection("Events")
events = ref.get()
for event in events:
    print(event.to_dict())
