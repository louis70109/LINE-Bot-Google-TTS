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


def get_all_collection(collection):
    return db.collection(collection).get()


def get_audios_collection(collection, vid: str):
    return db.collection(collection).where('vid', '==', vid).get()


def get_collection(collection, name):
    doc_ref = db.collection(collection).document(f"{collection}_{name}")
    if doc_ref.get().exists:
        return doc_ref.get().to_dict()
    return None


def create_audio(audio_dict):
    # id, name, bucket
    doc_ref = db.collection("audios").document(
        f"audios_{audio_dict.get('bucket')}_{audio_dict.get('name')}")
    doc_ref.set(audio_dict)
    return {}


def update_audio(audio_dict):
    # id, name, bucket
    doc_ref = db.collection("audios").document(
        f"audios_{audio_dict.get('bucket')}_{audio_dict.get('name')}")
    doc_ref.update(audio_dict)
    return {}


def create_subtitle(subtitle_dict):
    # vid, id, description, start_time, end_time
    doc_ref = db.collection("subtitles").document(
        f"subtitles_{subtitle_dict.get('vid')}_{subtitle_dict.get('id')}")
    doc_ref.set(subtitle_dict)
    return {}


def update_subtitle(subtitle_dict: dict):
    # vid, id, description, start_time, end_time
    doc_ref = db.collection("subtitles").document(
        f"subtitles_{subtitle_dict.get('vid')}_{subtitle_dict.get('id')}")
    doc_ref.update(subtitle_dict)
    return {}


def remove_subtitle(vid: str, id: str):
    # vid, id, description, start_time, end_time
    doc_ref = db.collection("subtitles").document(
        f"subtitles_{vid}_{id}")
    doc_ref.delete()
    return {}
