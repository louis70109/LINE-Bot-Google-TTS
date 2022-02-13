# Speech

- Create Cloud Storage
- [IAM & Admin](https://console.cloud.google.com/iam-admin)
  - Create a **Service Account**
  - Go to Service Account `KEYS` tab
  - ADD KEY -> Create a new key -> Select `JSON` -> Download it
  
  
# Speech to Text

- Use IAM key to access STT API.
- [code reference](https://cloud.google.com/speech-to-text/docs/samples/speech-transcribe-async-gcs#speech_transcribe_async_gcs-python)
  - set timeout to 15 seconds.
- `zh-TW` Language support from [doc](https://cloud.google.com/speech-to-text/docs/languages).
- `MP3` audio currently is BETA feature. It's not support in SDK now(2022/02).
  - LINE message audio `m4a` could force change `mp3`, and it was `16000` Hz.
  - In [doc](https://cloud.google.com/speech-to-text/docs/reference/rest/v1p1beta1/RecognitionConfig#AudioEncoding), `sampleRateHertz` supported `MP3`. 
  - So we could use `WEBM_OPUS` as **AudioEncoding** parameter.
  - Following code could recognize the audio which is from LINE message with `m4a` format.
```python
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
    sample_rate_hertz=16000,
    language_code="zh-TW",
)
```

## Dialogflow

- Set on your [Dialogflow Console](https://dialogflow.cloud.google.com/)
- Add Entities.
- Add Entities in Intents dialog.
- Add more and more phrases to train it. See [doc](https://cloud.google.com/dialogflow/es/docs/intents-training-phrases#annotation).

Get intents.

```python
intent = dict(response.query_result.parameters)
```

> Code from [Quick Start](https://cloud.google.com/dialogflow/es/docs/quick/api).

# LICENSE

MIT