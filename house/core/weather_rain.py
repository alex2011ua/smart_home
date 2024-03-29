"""
https://openweathermap.org/
"""
import os
import time
from datetime import date, timedelta

import requests

APPID_Weather = os.environ.get("APPID_Weather")
payload = {
    "lat": 50.40,
    "lon": 30.31,
    "appid": APPID_Weather,
    "units": "metric",
    "lang": "ru",
}


def weather_now():  # погода на сегодня и завтра
    """
    погода на сегодня и завтра
    :return:
    """
    payload["exclude"] = "minutely,hourly"
    url = "https://api.openweathermap.org/data/2.5/onecall"
    r = requests.get(url, params=payload)
    if r.status_code != 200:
        return {"status_code": r.status_code}
    d = r.json()

    context = {
        "icon": d["current"]["weather"][0]["icon"],
        "description": d["current"]["weather"][0]["description"],
        "temp": d["current"]["temp"],
        "wind": d["current"]["wind_speed"],
        "humidity": d["current"]["humidity"],
        "description_next": d["daily"][0]["weather"][0]["description"],
        "icon_next_day": d["daily"][0]["weather"][0]["icon"],
        "temp_next_morn": d["daily"][0]["temp"]["morn"],
        "temp_next_day": d["daily"][0]["temp"]["day"],
        "temp_next_eve": d["daily"][0]["temp"]["eve"],
        "pop_next": d["daily"][0]["pop"],
        "wind_speed_next": d["daily"][0]["wind_speed"],
        "status_code": r.status_code,
    }
    #  создаем спидок правительственных предупреждений
    if d.get("alerts"):
        context["alerts"] = []
        for item in d["alerts"]:
            context["alerts"].append(item["description"])
    print(__name__)
    return context


def weather_6_day():
    """
    Погода на  6 дней
    :return: summ of rain (Сумма воды которая выпадет за 3 дней)
    """
    payload["exclude"] = "current,minutely,hourly,alerts"
    url = "https://api.openweathermap.org/data/2.5/onecall"
    r = requests.get(url, params=payload)
    if r.status_code != 200:
        return {"status_code", r.status_code}
    d = r.json()

    summ_rain_3_day = 0.0
    summ_snow_3_day = 0.0
    for i in d["daily"][0:1]:
        if i.get("rain"):
            summ_rain_3_day += float(i["rain"])
        if i.get("snow"):
            summ_snow_3_day += float(i["snow"])

    min_temp = 100
    max_temp = -100
    for i in d["daily"][0:3]:
        if i["temp"]["min"] < min_temp:
            min_temp = i["temp"]["min"]
        if i["temp"]["max"] > max_temp:
            max_temp = i["temp"]["max"]

    tomorrow_date = date.today()
    context = {
        "tomorrow_date": tomorrow_date,
        "summ_rain_3_day": summ_rain_3_day,
        "summ_snow_3_day": summ_snow_3_day,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "status_code": r.status_code,
    }
    return context


def rain_yesterday():
    """
    погода на вчера
    :return: float sum_rain, datetime.date
    """
    start_Date = date.today()  # год, месяц, число
    timestamp = time.mktime(start_Date.timetuple())
    payload["exclude"] = "current"
    payload["dt"] =  int(timestamp)
    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"
    r = requests.get(url, params=payload)
    if r.status_code != 200:
        return {"status_code": r.status_code}
    d = r.json()

    sum_rain = 0
    sum_snow = 0
    min_temp = 100
    max_temp = -100
    for item in d["hourly"]:
        if item.get("rain"):
            sum_rain += item["rain"]["1h"]
        if item.get("snow"):
            sum_snow += item["snow"]["1h"]
        if item["temp"] > max_temp:
            max_temp = item["temp"]
        if item["temp"] < min_temp:
            min_temp = item["temp"]

    result_date = start_Date - timedelta(days=1)
    context = {
        "result_date": result_date,
        "sum_rain": sum_rain,
        "sum_snow": sum_snow,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "status_code": r.status_code,
    }
    return context

if __name__ == "__main__":
    loc_path = os.path.dirname(__file__)
    loc_path = os.path.split(loc_path)

    dotenv_path = os.path.join(loc_path[0], ".env")
    from dotenv import load_dotenv
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    APPID_Weather = os.environ.get("APPID_Weather")
    payload = {
        "lat": 50.40,
        "lon": 30.31,
        "appid": APPID_Weather,
        "units": "metric",
        "lang": "ru",
    }
    print(rain_yesterday())
    print(weather_6_day())
    print(__name__)