import os
from fastapi.testclient import TestClient

from main import app

from utils.common import contents_dict_to_vtt

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_read_bot():
    import base64
    import hashlib
    import hmac

    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    body = '{"events":[],"destination":"U000000000000000000000003d9"}'
    hash = hmac.new(channel_secret.encode('utf-8'),
                    body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    response = client.post(
        url="/webhooks/line",
        data=body,
        headers={
            "Content-Type": "multipart/form-data",
            'X-Line-Signature': signature.decode('UTF-8')
        })

    assert response.url == 'http://testserver/webhooks/line'
    assert response.status_code == 200
    assert response.json() == 'OK'


# class TestClient(unittest.TestCase):
#     def setUp(self):
#         pass
#
#     def test_read_main(self):
#         response = client.get("/")
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"message": "Hello World!"})


def test_contents_to_vtt():
    contents = [{
        "description": "我覺, 真是, 不得了。",
        "vid": "7964313717",
        "id": 0,
        "end_time": "0:00:59.200",
        "start_time": "0:00:00"},
        {"id": 1,
         "end_time": "0:01:59.600",
         "start_time": "0:00:59.900",
         "vid": "7964217a13717",
         "description": "Ok有經驗？"}]
    res = contents_dict_to_vtt(contents)

    expect = "WEBSTT\n\n0\n0:00:00 --> 0:00:59.200\n我覺, 真是, 不得了。\n\n1\n0:00:59.900 --> 0:01:59.600\nOk有經驗？\n\n"
    assert res == expect
