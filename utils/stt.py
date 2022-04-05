import datetime
import os

import requests


def time_transfer(seconds):
    return str(datetime.timedelta(seconds=seconds))


def audio_string_time(alternative) -> (str, str):
    word_len = len(alternative.words)
    start_time, end_time = 0, 1
    for index in range(word_len):
        word = alternative.words
        if index == 0:
            start_time = word[0].start_time.total_seconds()
        if index == word_len - 1:
            end_time = word[index].end_time.total_seconds()
    return time_transfer(start_time), time_transfer(end_time)


def intent_format_srt(response) -> str:
    return_value = '尚無字串'
    count = 0
    contents = ''
    for result in response.results:
        print(count)
        alternative = result.alternatives[0]
        start, end = audio_string_time(alternative)
        contents += f'{str(count)}\n{start} --> {end}\n{alternative.transcript}\n\n'
        # The first alternative is the most likely one for this portion.
        # print(u"Transcript: {}".format(alternative.transcript))
        count += 1
        # print("Confidence: {}".format(alternative.confidence))
    # with open("a1.srt", "w") as f:
    #     f.writelines(contents)
    return contents


def create_hackmd(content):
    req = requests.post(url="https://api.hackmd.io/v1/notes",
                        headers={'Authorization': f'Bearer {os.getenv("HACKMD_TOKEN")}'}, json={
            "title": "New note",
            "content": content,
            "readPermission": "owner",
            "writePermission": "owner",
            "commentPermission": "everyone"
        })
    print(req.json())


def transcribe_gcs():
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()
    gcs_uri = f"gs://{os.getenv('GOOGLE_BUCKET')}/Sequence.mp3"
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
