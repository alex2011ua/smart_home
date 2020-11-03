'''
https://openweathermap.org/
'''

import requests


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
    return summ


#  погода на сегодня
def weather_now():
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

def weather():
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
    return summ
if __name__ == "__main__":
    import pprint
    pprint.pprint(weather())
