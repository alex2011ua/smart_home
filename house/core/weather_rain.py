'''
https://openweathermap.org/
'''

import requests

from datetime import date, timedelta
import time

import os
APPID_Weather = os.environ.get('APPID_Weather')
def weather_rain_summ():
    '''
    :return: summ of rain (Сумма воды которая выпадет за 3 дней)
    '''
    payload = {'lat': 50.40,
               'lon': 30.31,
               'appid': APPID_Weather,
               'units': 'metric',
               'lang': 'ru',
               'exclude': 'current,minutely,hourly,alerts'
               }
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    r = requests.get(url, params = payload)
    d = r.json()
    summ = 0.0
    print(len(d["daily"][0:3]))
    for i in d["daily"]:

        if i.get('rain'):
            summ += float(i['rain'])
    start_Date = date.today()  # год, месяц, число
    tomorrow_date = start_Date + timedelta(days = 1)
    return summ, tomorrow_date


#  погода на сегодня
def weather_now():
    '''
    погода на сегодня
    :return:
    '''
    payload = {'lat': 50.40,
               'lon': 30.31,
               'appid': APPID_Weather,
               'units': 'metric',
               'lang': 'ru',
               'exclude': 'minutely,hourly,daily',
               }
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    r = requests.get(url, params = payload)
    d = r.json()

    context = {
        'icon':         d['current']['weather'][0]['icon'],
        'description':  d['current']['weather'][0]['description'],
        'temp':         d['current']['temp'],
        'wind':         d['current']['wind_speed']

    }
    #  создаем спидок правительственных придупреждений
    if d.get('alerts'):
        context['alerts'] =[]
        for item in d['alerts']:
            context['alerts'].append(item['description'])

    return context


def rain_yesterday():
    '''
    сумму воды и вчерашнюю дату
    :return: float sum_rain, datetime.date
    '''
    start_Date = date.today()  # год, месяц, число
    result_date = start_Date - timedelta(days = 1)
    timestamp = time.mktime(start_Date.timetuple())
    payload = {'lat': 50.40,
               'lon': 30.31,
               'appid': APPID_Weather,
               'units': 'metric',
               'dt': int(timestamp),
               'lang': 'ru',
               'exclude': 'current'
               }
    url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
    r = requests.get(url, params = payload)
    d = r.json()
    sum_rain = 0
    count = 0
    for item in d['hourly']:
        count += 1
        if item.get('rain'):
            sum_rain += item['rain']


    return sum_rain, result_date


def weather_min():
    '''
    :return: summ of rain (Сумма воды которая выпадет за 3 дней)
    '''
    payload = {'lat': 50.40,
               'lon': 30.31,
               'appid': 'd16e0dacb5474e43829b385c7102e12d',
               'units': 'metric',
               'lang': 'ru',
               'exclude': 'current,minutely,hourly,alerts'
               }
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    r = requests.get(url, params = payload)
    d = r.json()
    summ = 0.0
    for i in d["daily"][0:3]:
        if i.get('rain'):
            summ += float(i['rain'])

    min_temp = 0
    for i in d["daily"]:
        print(i['temp']['min'])



    start_Date = date.today()  # год, месяц, число
    tomorrow_date = start_Date + timedelta(days = 1)
    return summ, tomorrow_date




if __name__ == "__main__":
    import pprint
    pprint.pprint(weather_())
