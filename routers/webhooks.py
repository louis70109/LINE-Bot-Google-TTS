import datetime
import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Header, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage, \
    AudioMessage
from pydantic import BaseModel

from utils.common import write_audio_file, google_tts, detect_intent_texts
from utils.firebase import create_user, create_drink, get_user

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

router = APIRouter(
    prefix="/webhooks",
    tags=["chatbot"],
    responses={404: {"description": "Not found"}},
)


class Line(BaseModel):
    destination: str
    events: List[Optional[None]]


@router.post("/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="chatbot handle body error.")
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    user_id = event.source.user_id
    user = line_bot_api.get_profile(user_id)

    print(get_user(user_id))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


@handler.add(MessageEvent, message=AudioMessage)
def audio_text(event):
    user_id = event.source.user_id
    user = line_bot_api.get_profile(user_id)
    create_user({
        'id': user.user_id,
        'picture_url': user.picture_url,
        'name': user.display_name,
    })
    write_audio_file(event.message.id, user_id)
    speech_content = google_tts(user_id)
    intent = detect_intent_texts(
        project_id=os.getenv('DIALOGFLOW_PROJECT_ID'),
        session_id=user_id,
        texts=speech_content, language_code='zh-TW'
    )

    create_drink({
        'uid': user_id,
        'item': intent.get('item'),
        'sugar': intent.get('sugar'),
        'ice': intent.get('ice')
    }, date=datetime.date.today())
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(
            {
                'uid': user_id,
                'item': intent.get('item'),
                'sugar': intent.get('sugar'),
                'ice': intent.get('ice'),
                'date': datetime.date.today()}
        ))
    )
