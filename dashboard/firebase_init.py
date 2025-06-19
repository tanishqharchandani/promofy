import os
import firebase_admin
from firebase_admin import credentials, storage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cred_path = os.path.join(BASE_DIR, "firebase_credentials.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'promofy-mvp.firebasestorage.app'  # ✅ Use this bucket name
    })
