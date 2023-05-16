import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Use a service account
cred = credentials.Certificate(
    'firestore491test-firebase-adminsdk-7l56g-2cd92c9238.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
