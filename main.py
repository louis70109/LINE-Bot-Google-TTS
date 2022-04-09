import os
import tempfile
import uuid

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

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from utils.stt import transcribe_gcs, intent_format_srt, create_hackmd
from utils.firebase import get_collection, create_audio
from routers import webhooks, audios, subtitles

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(webhooks.router)
app.include_router(audios.router)
app.include_router(subtitles.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/liff", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/upload")
async def speech_service():
    bucket = os.getenv('GOOGLE_BUCKET')
    name = 'Sequence'
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
    create_hackmd(contents)

    return "Done"


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0",
        port=5000, reload=True
    )
