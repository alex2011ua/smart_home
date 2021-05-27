from .raspberry import button
from myviberbot.viber_bot import send_viber
from .Telegram import bot
from datetime import datetime
from .models import Message, DHT_MQ, Setting
from django.core.exceptions import ObjectDoesNotExist


def button_analiz(DEBUG):
    """Если меняется состояние кнопка - шлем сообщение в бот"""

    date_now = datetime.now()
    context = button(DEBUG)  # текущее состояние  датчиков входа
    if DEBUG:
        date_now = datetime(2021, 3, 29, 21, 0, 0)
    try:
        dor = Message.objects.get(controller_name='dor')
        garaz = Message.objects.get(controller_name='garaz')
    except ObjectDoesNotExist:
        dor = Message.objects.create(controller_name='dor',
                                     date_message=datetime(2000, 1, 1),
                                     value_int=0)
        garaz = Message.objects.create(controller_name='garaz',
                                       date_message=datetime(2000, 1, 1),
                                       value_int=0)

    # извещение о смене состоянию входов
    if context['Garaz'] != garaz.state:
        garaz.state = context['Garaz']
        garaz.date_message = date_now
        if context['Garaz']:
            garaz.label = 'Открыт гараж'
        else:
            garaz.label = 'Закрыт гараж'
        garaz.save()
        bot.send_message(garaz.label)

    if context['Dor_street'] != dor.state:
        dor.state = context['Dor_street']
        dor.date_message = date_now
        if context['Dor_street']:
            dor.label = 'Открыта дверь'
        else:
            dor.label = 'Закрыта дверь'
        dor.save()
        bot.send_message(dor.label)
    # Если ночью открывается дверь - шлем сообщение в бот
    if date_now.hour <= 5 or date_now.hour > 23:
        if context['Garaz'] and garaz.value_int == 0:
            bot.send_message('Открыт гараж ночью')
            send_viber('Открыт гараж ночью')
            garaz.value_int = 1
            garaz.save()
        if context['Dor_street'] and dor.value_int == 0:
            bot.send_message('Открыта дверь ночью')
            send_viber('Открыта дверь ночью')
            dor.value_int = 1
            dor.save()
    if dor.value_int == 1 and date_now.hour > 5:
        dor.value_int = 0
        dor.save()
    if garaz.value_int == 1 and date_now.hour > 5:
        garaz.value_int = 0
        garaz.save()
    # напоминание вечером закрыть входы
    vecher(date_now, context['Garaz'], context['Dor_street'])


def vecher(now, garaz, dor):
    list_to_hour = [21, 22, 23, 0]
    if (now.hour in list_to_hour) and now.minute == 0:
        if garaz == 1:
            bot.send_message('Нужно на ночь закрыть гараж')
            send_viber('Нужно на ночь закрыть гараж')
        if dor == 1:
            bot.send_message('Нужно на ночь закрыть дверь')
            send_viber('Нужно на ночь закрыть дверь')


def gaz_analiz(MQ4, MQ135):
    """Если значения датчиков превышают пороговые - шлем сообщение в бот"""
    try:
        gaz = Message.objects.get(controller_name='gaz')
    except ObjectDoesNotExist:
        gaz = Message.objects.create(controller_name='gaz',
                                     date_message=datetime(2000, 1, 1))
    date_now = datetime.now()
    time_delta = (date_now - gaz.date_message) // 60  # minutes
    if time_delta.seconds > 60:
        bot.send_message('Завышены показания газовый датчиков')
        bot.send_message(f'MQ-4 - {MQ4}, MQ-135 - {MQ135}')
        gaz.date_message = date_now
        gaz.controller_name = 'gaz'
        gaz.label = "Allarm"
        gaz.value_int = MQ4 + MQ135
        gaz.save()


def temp_alert():
    """
    Проверка критичных показаний температуры
    :return:
    """
    temp = DHT_MQ.objects.all().order_by('-date_t_h')[0]  # arduino state
    if temp.temp_gaz <= 22:
        bot.send_message(f"Температура котельной: {temp.temp_voda}")
