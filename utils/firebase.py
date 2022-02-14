import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_user(id):
    doc_ref = db.collection("users").document(f"user_{id}")

    return doc_ref.get().to_dict()


def create_user(user_dict):
    doc_ref = db.collection("users").document(f"user_{user_dict.get('id')}")
    doc_ref.set(user_dict)
    return {}


def create_drink(drink_dict, date):
    doc_ref = db.collection("drinks").document(f"{date}drink_{drink_dict.get('uid')}")
    doc_ref.set(drink_dict)
    return {}
