# Speech

- Create Cloud Storage

![](https://github.com/louis70109/LINE-Bot-Google-TTS/blob/a396f745c7e7b8e3de33c816a6cb2aac2df6945c/readme_img/storage.png)

- [IAM & Admin](https://console.cloud.google.com/iam-admin)
  - Create a **Service Account**
  - Go to Service Account `KEYS` tab
  - ADD KEY -> Create a new key -> Select `JSON` -> Download it

![](https://github.com/louis70109/LINE-Bot-Google-TTS/blob/a396f745c7e7b8e3de33c816a6cb2aac2df6945c/readme_img/role.png)

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

![](https://github.com/louis70109/LINE-Bot-Google-TTS/blob/a396f745c7e7b8e3de33c816a6cb2aac2df6945c/readme_img/entity.png)

- Add Entities in Intents dialog.
- Add more and more phrases to train it. See [doc](https://cloud.google.com/dialogflow/es/docs/intents-training-phrases#annotation).

![](https://github.com/louis70109/LINE-Bot-Google-TTS/blob/a396f745c7e7b8e3de33c816a6cb2aac2df6945c/readme_img/dialog.png)

Get intents.

```python
intent = dict(response.query_result.parameters)
```

> Code from [Quick Start](https://cloud.google.com/dialogflow/es/docs/quick/api).

## Binding STT and Dialogflow Result

![](https://github.com/louis70109/LINE-Bot-Google-TTS/blob/a396f745c7e7b8e3de33c816a6cb2aac2df6945c/readme_img/result.PNG)

## Save data to Firebase

> [refs](https://firebase.google.com/docs/firestore/query-data/get-data#python)

- Project setting -> Service Account -> Add -> Choose Python -> Create Firebase Token JSON to current project.
  - 中文: 專案設定 -> 服務帳戶 -> 建立 -> 選擇 Python -> 產生金鑰 -> 到專案下
- create a Firestore Database and collection.

```python
import firebase_admin  
from firebase_admin import credentials  
from firebase_admin import firestore  
  
cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS'))  
firebase_admin.initialize_app(cred)  
db = firestore.client()  
  
  
def create_user(user_dict):  
    doc_ref = db.collection("users").document(f"user_{user_dict.get('id')}")  
    doc_ref.set(user_dict)  
    return {}
```

# Quick Start

Install packages.

```bash
pip install -r requrements.txt
```

Copy and fill environment variables.(`.env`)

```
cp .env.sample .env
```

Run application.

```
python main.py
```

Change LINE Bot development webhook url.

```
sh change_bot_url.sh BOT_ACCESS_TOKEN https://YOUR_DOMAIN/webhooks/line
```

## By Docker

TODO

# LICENSE

MIT
