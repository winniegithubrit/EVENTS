import firebase_admin
from firebase_admin import credentials, storage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH')
FIREBASE_BUCKET_NAME = os.getenv('FIREBASE_BUCKET_NAME')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred, {
    'storageBucket': FIREBASE_BUCKET_NAME  
})


bucket = storage.bucket()
