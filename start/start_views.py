from django.shortcuts import render

from start.models import Avto
from house.core.Telegram import bot
from django.views import View
from .avto_api import get_list_car
import json



