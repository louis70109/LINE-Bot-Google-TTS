import os

from linebot import LineBotApi
from google.cloud import speech


def write_audio_file(message_id):
    line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
    message_content = line_bot_api.get_message_content(message_id)
    # with open('./abc.mp3', 'wb') as fd:
    #     for chunk in message_content.iter_content():
    #         fd.write(chunk)

def google_tts():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_service_key.json'
    speech_client = speech.SpeechClient()

    # Example 1 & 2. Transcribe Local Media File
    # File Size: < 10mbs, length < 1 minute

    ## Step 1. Load the media files
    media_file_name_mp3 = './abc.mp3'

    with open(media_file_name_mp3, 'rb') as f1:
        byte_data_mp3 = f1.read()
    audio_mp3 = speech.RecognitionAudio(content=byte_data_mp3)


    ## Step 2. Configure Media Files Output
    config_mp3 = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        enable_automatic_punctuation=True,
        language_code='zh-TW'
    )

    ## Step 3. Transcribing the RecognitionAudio objects
    response_standard_mp3 = speech_client.recognize(
        config=config_mp3,
        audio=audio_mp3
    )

    print(response_standard_mp3)

    # # Example 3: Transcribing a long media file
    # media_uri = 'gs://speech-to-text-media-files/Steve Job 2005 Commencement Speech.wav'
    # long_audi_wav = speech.RecognitionAudio(uri=media_uri)
    #
    # config_wav_enhanced = speech.RecognitionConfig(
    #     sample_rate_hertz=48000,
    #     enable_automatic_punctuation=True,
    #     language_code='en-US',
    #     use_enhanced=True,
    #     model='video'
    # )
    #
    # operation = speech_client.long_running_recognize(
    #     config=config_wav,
    #     audio=long_audi_wav
    # )
    # response = operation.result(timeout=90)
    # print(response)
    #
    # for result in response.results:
    #     print(result.alternatives[0].transcript)
    #     print(result.alternatives[0].confidence)
    #     print()