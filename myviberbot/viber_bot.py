from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
import os
from dotenv import load_dotenv
from house.core.Telegram import bot

from viberbot.api.messages import (TextMessage, PictureMessage)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
token = os.getenv('viber_token', os.environ.get('viber_token'))
bot_configuration = BotConfiguration(
	name='AlexUA',
	avatar='http://alexua.pp.ua/static/start/favico.jpg',
	auth_token=token
)
viber = Api(bot_configuration)
bot.send_message('create viber,  '+token)
