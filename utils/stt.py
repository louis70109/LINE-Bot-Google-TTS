import datetime
import os

import jieba
import requests
from google.cloud import storage

from utils.firebase import get_collection, update_subtitle, create_subtitle


def time_transfer(seconds) -> str:
    # example: 2:46:40.100
    time = str(datetime.timedelta(seconds=seconds))[:11]
    import re
    if re.search("[0-9]*:[0-9]+:[0-9]+", time) and len(time) == 7:
        time_obj = time.split(":")
        time = time_obj[0]+":"+time_obj[1]+":"+time_obj[2]+".000"
    return time


def audio_string_time(alternative) -> (str, str):
    word_len = len(alternative.words)
    start_time, end_time = 0, 1
    for index in range(word_len):
        word = alternative.words
        if index == 0:
            start_time = word[0].start_time.total_seconds()
        if index == word_len - 1:
            end_time = word[index].end_time.total_seconds()
    print('Google STT time/ arrange done.')
    return time_transfer(start_time), time_transfer(end_time)


def intent_format_srt(audio, response) -> list:
    count = 0
    contents = []
    for result in response.results:
        subtitles: list = get_collection('subtitles', f"{audio.get('id')}_{count}")

        alternative = result.alternatives[0]
        start, end = audio_string_time(alternative)
        seg_list = jieba.cut_for_search(alternative.transcript)

        sub_dict = {
            'vid': audio.get('id'),
            'id': count,
            'description': ", ".join(seg_list),
            'start_time': start,
            'end_time': end
        }
        if subtitles is None:
            print('Creating')
            create_subtitle(sub_dict)
        else:
            print('Updating')
            update_subtitle(sub_dict)

        contents.append(sub_dict)
        count += 1
    print('Subtitle format done.')
    return contents


def create_hackmd(content):
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('Start upload Note' + current_time)
    content = f'---\ntitle: 字幕{current_time}\n---\n\n' + content
    requests.post(url="https://api.hackmd.io/v1/notes",
                  headers={'Authorization': f'Bearer {os.getenv("HACKMD_TOKEN")}'}, json={
            "title": "New note",
            "content": content,
            "readPermission": "everyone",
            "writePermission": "owner",
            "commentPermission": "everyone"
        })
    print('HackMD upload done.')


def transcribe_gcs(bucket, audio):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()
    gcs_uri = f"gs://{bucket}/{audio}"
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48000,
        language_code="zh-TW",
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()
    return response
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

