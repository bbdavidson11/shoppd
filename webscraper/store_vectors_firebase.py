import firebase_admin
from firebase_admin import credentials

# Firebase initialization
cred = credentials.Certificate("firebasecred.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'shop-d-ea02c.appspot.com'
})