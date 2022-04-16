import os

from linebot import LineBotApi
from google.cloud import speech, storage, dialogflow


def upload_data_to_gcs(bucket_name, data, target_key, meta=None):
    if type(data) == str:
        data = data.encode('big5')

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(target_key)
        blob.upload_from_string(data, content_type=meta)
        return blob.public_url

    except Exception as e:
        print(e)

    return None


def write_audio_file(message_id, user_id):
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
    try:
        message_content = line_bot_api.get_message_content(message_id)
    except Exception:
        raise Exception('Message content not found.')

    total = b''
    for chunk in message_content.iter_content():
        total += chunk

    upload_data_to_gcs(os.getenv('GOOGLE_BUCKET'), total, f'{user_id}.mp3')


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    intent = dict(response.query_result.parameters)
    if intent.get('drink') and intent.get('sugar') and intent.get('ice'):
        return {
            'item': intent.get('drink'),
            'sugar': intent.get('sugar'),
            'ice': intent.get('ice')
        }
    else:
        return None


def contents_dict_to_vtt(contents):
    # [{
    #         "description": "我覺不得了。",
    #         "vid": "7964313717",
    #         "id": 0,
    #         "end_time": "0:00:59.200",
    #         "start_time": "0:00.00"},
    #         {"id": 1,
    #          "end_time": "0:01:59.600",
    #          "start_time": "0:00:59.900",
    #          "vid": "7964217a13717",
    #          "description": "Ok有經驗？"}]
    result = 'WEBVTT\n\n'
    content_len, idx, count = len(contents), 0, 0

    # Arrange firebase data list sequence
    while True:
        try:
            content = contents[idx]
            if content.get("id") == count:
                result += f'{content.get("id")}\n{content.get("start_time")} --> {content.get("end_time")}\n{content.get("description")}\n\n'
                contents.pop(idx)
                count += 1
                idx = 0
            else:
                idx += 1
            if len(contents) == 0:
                break
        except IndexError:
            break

    return result
