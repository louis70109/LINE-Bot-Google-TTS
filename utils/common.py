import os

from linebot import LineBotApi
from google.cloud import speech,  storage, dialogflow


def upload_data_to_gcs(bucket_name, data, target_key):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        bucket.blob(target_key).upload_from_string(data)
        return bucket.blob(target_key).public_url

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


def google_tts(user_id):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = f"gs://{os.getenv('GOOGLE_BUCKET')}/{user_id}.mp3"

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=16000,
        language_code="zh-TW",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=15)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
        # if > 0.9
        return result.alternatives[0].transcript


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
    print(intent)
    if intent.get('self') and intent.get('drink'):
        return f"想喝「{intent.get('drink')}」是不是"
    return "我聽不懂喔"
