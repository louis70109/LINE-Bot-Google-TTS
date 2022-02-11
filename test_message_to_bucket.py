from google.cloud import storage
from linebot import LineBotApi
import os

line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
message_content = line_bot_api.get_message_content('MESSAGE_ID')
message_content.iter_content()


def upload_data_to_gcs(bucket_name, data, target_key):
    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        bucket.blob(target_key).upload_from_string(data)
        return bucket.blob(target_key).public_url

    except Exception as e:
        print(e)

    return None


print(type(message_content.iter_content()))

total = b''
for chunk in message_content.iter_content():
    total += chunk
print(total)
upload_data_to_gcs('YOUR_GOOGLE_BUCKET', total, 'hello.mp3')
