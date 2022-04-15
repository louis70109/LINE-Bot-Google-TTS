import os
import tempfile
import uuid

import requests

from utils.common import upload_data_to_gcs, contents_dict_to_vtt

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

google_temp = tempfile.NamedTemporaryFile(suffix='.json')
fire_temp = tempfile.NamedTemporaryFile(suffix='.json')
try:
    GOOGLE_KEY = os.environ.get('GOOGLE_KEY', '{}')
    google_temp.write(GOOGLE_KEY.encode())
    google_temp.seek(0)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_temp.name

    FIRE_KEY = os.environ.get('FIREBASE_KEY', '{}')
    fire_temp.write(FIRE_KEY.encode())
    fire_temp.seek(0)
    os.environ['FIREBASE_CREDENTIALS'] = fire_temp.name
except:
    google_temp.close()
    fire_temp.close()

import uvicorn

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from utils.stt import transcribe_gcs, intent_format_srt
from utils.firebase import get_collection, create_audio
from routers import webhooks, audios, subtitles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(webhooks.router)
app.include_router(audios.router)
app.include_router(subtitles.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/upload/{name}")
async def speech_service(name: str):
    bucket = os.getenv('GOOGLE_BUCKET')
    audio = get_collection('audios', f"{bucket}_{name}")
    if audio == {} or audio is None:  # empty
        audio = {
            'id': uuid.uuid4().hex,
            'bucket': bucket,
            'name': name
        }
        create_audio(audio)
    intent = transcribe_gcs(bucket, f'{name}.mp3')

    contents = intent_format_srt(audio, intent)
    vtt_string_result = contents_dict_to_vtt(contents)
    upload_data_to_gcs(bucket, vtt_string_result, f'{name}.vtt')
    return "Done"


@app.post("/upload")
def upload_file(info: dict):
    # [{
    #         "description": "我覺",
    #         "vid": "7964313717",
    #         "id": 0,
    #         "end_time": "0:00:59.200",
    #         "start_time": "0:00:00"}]
    vtt_string = contents_dict_to_vtt(info.get("contents"))
    res = upload_data_to_gcs(os.getenv('GOOGLE_BUCKET'), vtt_string, f'{info.get("name")}.vtt')
    return res


@app.get("/bucket")
def speech_service():
    return os.getenv('GOOGLE_BUCKET')


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0",
        port=5000, reload=True
    )
