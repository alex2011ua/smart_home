import datetime
import os

import requests
from django.core.exceptions import ObjectDoesNotExist
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
apy_key = os.getenv("apy_key", os.environ.get("apy_key"))


url_search = "https://developers.ria.com/auto/search"
url_info = "https://developers.ria.com/auto/info"

def get_avto(id):
    params = {
        "api_key": apy_key,
        "auto_id": id,
    }
    avto = requests.get(url_info, params=params)
    if avto.status_code == 200:
        j = avto.json()
        return j
    else:
        return {"status": avto.status_code}  # 429 (слишком много запросов)



def get_list_car(params):
    """
    получает словарь параметров запроса и возвращает ответ
    :param params: dict словарь параметров запроса
    :return: dict количество авто в запросе и список ID авто
    """
    payload = {
        "api_key": apy_key,
        "category_id": 1,
        "s_yers": [2016],
        "po_yers": [2017],
        "price_ot": 11000,
        "price_do": 13500,
        "type": [
            # 1,  # бенз
            # 2,  # дизель
            # 4,  # газ
            6,  # электро
        ],
        "gearbox": [
            1,  # механика
            2,  # автомат
            3,  # титпроник
        ],
        "countpage": 100,
        "abroad": 2,  # Не отображать авто которые находяться не в Украине
        "custom": 1,  # Не отображать нерастаможенные авто
        "with_photo": 1,  # Только с фото
        "damage": 1,  # не поврежден
    }

    payload.update(params)
    zapros_po_param = requests.get(url_search, params=payload)

    if zapros_po_param.status_code == 200:
        j = zapros_po_param.json()
        count_avto = int(j["result"]["search_result"]["count"])
        list_cars = j["result"]["search_result"]["ids"]
        return {"status": 200, "count_avto": count_avto, "list_cars": list_cars}
    else:
        return {"status": zapros_po_param.status_code}  # 429 (слишком много запросов)

# https://developers.ria.com/auto/search?api_key=YOUR_API_KEY&category_id=1&bodystyle%5B0%5D=3&bodystyle%5B4%5D=2&marka_id%5B0%5D=79&model_id%5B0%5D=0&s_yers%5B0%5D=2010&po_yers%5B0%5D=2017&marka_id%5B1%5D=84&model_id%5B1%5D=0&s_yers%5B1%5D=2012&po_yers%5B1%5D=2016&brandOrigin%5B0%5D=276&brandOrigin%5B1%5D=392&price_ot=1000&price_do=60000&currency=1&auctionPossible=1&with_real_exchange=1&with_exchange=1&exchange_filter%5Bmarka_id%5D=0&exchange_filter%5Bmodel_id%5D=0&state%5B0%5D=1&city%5B0%5D=0&state%5B1%5D=2&city%5B1%5D=0&state%5B2%5D=10&city%5B2%5D=0&abroad=2&custom=1&auto_options%5B477%5D=477&type%5B0%5D=1&type%5B1%5D=2&type%5B3%5D=4&type%5B7%5D=8&gearbox%5B0%5D=1&gearbox%5B1%5D=2&gearbox%5B2%5D=3&engineVolumeFrom=1.4&engineVolumeTo=3.2&powerFrom=90&powerTo=250&power_name=1&countpage=50&with_photo=1

if __name__ == "__main__":
    os.chdir("..")
    dotenv_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    apy_key = os.getenv("apy_key", os.environ.get("apy_key"))

    params = {
        "marka_id": 55,
        "model_id": 36565,



    }

    print(get_list_car(params=params))
    print(get_avto(31372826))

def check():
    params = {
        "marka_id": 55,  # nisan
        "model_id": 36565,  # Leaf
    }
    list_all_car = get_list_car(params=params)['list_cars']
    return list_all_car

