import os

from linebot import LineBotApi
from google.cloud import speech
from google.cloud import storage


def upload_data_to_gcs(bucket_name, data, target_key):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        bucket.blob(target_key).upload_from_string(data)
        return bucket.blob(target_key).public_url

    except Exception as e:
        print(e)

    return None


def write_audio_file(message_id):
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
    message_content = line_bot_api.get_message_content(message_id)
    total = b''
    for chunk in message_content.iter_content():
        total += chunk

    upload_data_to_gcs(os.getenv('GOOGLE_BUCKET'), total, 'hello.mp3')


def google_tts():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = f"gs://{os.getenv('GOOGLE_BUCKET')}/hello.mp3"

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=16000,
        language_code="zh-TW",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))
