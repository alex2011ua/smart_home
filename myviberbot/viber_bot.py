from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
import os
from dotenv import load_dotenv
from viberbot.api.messages import (TextMessage, PictureMessage)
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot_configuration = BotConfiguration(
	name='AlexUA',
	avatar='http://alexua.pp.ua/static/start/favico.jpg',
	auth_token= os.getenv('viber_token', os.environ.get('viber_token'))
)
viber = Api(bot_configuration)

# creation of text message
text_message = TextMessage(text="sample text message!")

# creation of picture message
picture_message = PictureMessage(text="Check this", media="http://site.com/img.jpg")
