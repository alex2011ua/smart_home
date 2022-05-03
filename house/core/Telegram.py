import os

import requests
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv("TOKEN", os.environ.get("TOKEN"))


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.api_setWebhook = (
            "https://api.telegram.org/bot{}/setWebhook?url=https://alexua.pp.ua:8443/{}/".format(
                token, token
            )
        )

    def send_message(self, text, chat_id=810867568):
        params = {"chat_id": chat_id, "text": text}
        method = "sendMessage"
        resp = requests.post(self.api_url + method, params)
        return resp

    def set_webhook(self):
        resp = requests.get(self.api_setWebhook)
        print(resp.text)


bot = TelegramBot(token)
