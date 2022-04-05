import os
import tempfile

from utils.stt import transcribe_gcs, intent_format_srt, create_hackmd

if os.getenv('API_ENV') != 'production':
    from dotenv import load_dotenv

    load_dotenv()

import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routers import webhooks

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(webhooks.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/liff", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/upload")
async def speech_service():
    intent = transcribe_gcs()
    contents = intent_format_srt(intent)
    create_hackmd(contents)

    return "Done"


if __name__ == "__main__":
    temp = tempfile.NamedTemporaryFile(suffix='.json')
    try:
        SOME_KEY = os.environ.get('GOOGLE_KEY', '{}')
        temp.write(SOME_KEY.encode())
        temp.seek(0)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp.name

        uvicorn.run(
            "main:app", host="0.0.0.0",
            port=5000, reload=True
        )
    finally:
        temp.close()
