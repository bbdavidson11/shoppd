import firebase_admin
from firebase_admin import credentials

# Any python file that uses firestore will simply import this folder
# not sure why stack overflow solutions aren't working while this is.
cred = credentials.Certificate('ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'shop-d-ea02c.appspot.com'
})