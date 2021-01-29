import requests

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
apy_key = os.getenv('apy_key', os.environ.get('apy_key'))
bodystyles = [
  {
    "name": "Седан",
    "value": 3
  },
  {
    "name": "Внедорожник / Кроссовер",
    "value": 5
  },
  {
    "name": "Минивэн",
    "value": 8
  },
  {
    "name": "Хэтчбек",
    "value": 4
  },
  {
    "name": "Универсал",
    "value": 2
  },
  {
    "name": "Купе",
    "value": 6
  },
  {
    "name": "Легковой фургон (до 1,5 т)",
    "value": 254
  },
  {
    "name": "Кабриолет",
    "value": 7
  },
  {
    "name": "Пикап",
    "value": 9
  },
  {
    "name": "Лифтбек",
    "value": 307
  },
  {
    "name": "Лимузин",
    "value": 252
  },
  {
    "name": "Другой",
    "value": 28
  },
  {
    "name": "Родстер",
    "value": 315
  }
]
brandOrigin = [
  {
    "name": "Abarth",
    "value": 5166
  },
  {
    "name": "Acura",
    "value": 98
  },
  {
    "name": "Adler",
    "value": 2396
  },
  {
    "name": "Aero",
    "value": 5165
  },
  {
    "name": "Aixam",
    "value": 2
  },
  {
    "name": "Alfa Romeo",
    "value": 3
  },
  {
    "name": "Alpine",
    "value": 100
  },
  {
    "name": "Altamarea",
    "value": 3988
  },
  {
    "name": "AMC",
    "value": 5821
  },
  {
    "name": "Anaig",
    "value": 5769
  },
  {
    "name": "Armstrong Siddeley",
    "value": 5276
  },
  {
    "name": "Aro",
    "value": 101
  },
  {
    "name": "Artega",
    "value": 3105
  },
  {
    "name": "Asia",
    "value": 4
  },
  {
    "name": "AsiaStar",
    "value": 5793
  },
  {
    "name": "Aston Martin",
    "value": 5
  },
  {
    "name": "ATS Corsa",
    "value": 6160
  },
  {
    "name": "Audi",
    "value": 6
  },
  {
    "name": "Austin",
    "value": 7
  },
  {
    "name": "Austin-Healey",
    "value": 4355
  },
  {
    "name": "Autobianchi",
    "value": 102
  },
  {
    "name": "Avia",
    "value": 2077
  },
  {
    "name": "BAIC",
    "value": 55051
  },
  {
    "name": "Baojun",
    "value": 6228
  },
  {
    "name": "Baoya",
    "value": 5245
  },
  {
    "name": "Barkas (Баркас)",
    "value": 103
  },
  {
    "name": "Baw",
    "value": 1540
  },
  {
    "name": "Beijing",
    "value": 105
  },
  {
    "name": "Bentley",
    "value": 8
  },
  {
    "name": "Bertone",
    "value": 106
  },
  {
    "name": "Bio Auto",
    "value": 3127
  },
  {
    "name": "Blonell",
    "value": 108
  },
  {
    "name": "BMW",
    "value": 9
  },
  {
    "name": "BMW-Alpina",
    "value": 99
  },
  {
    "name": "Bollinger",
    "value": 6310
  },
  {
    "name": "Borgward",
    "value": 5240
  },
  {
    "name": "Brilliance",
    "value": 329
  },
  {
    "name": "Bristol",
    "value": 10
  },
  {
    "name": "Bugatti",
    "value": 109
  },
  {
    "name": "Buick",
    "value": 110
  },
  {
    "name": "BYD",
    "value": 386
  },
  {
    "name": "Byton",
    "value": 6260
  },
  {
    "name": "Cadillac",
    "value": 11
  },
  {
    "name": "Caterham",
    "value": 3221
  },
  {
    "name": "Chana",
    "value": 407
  },
  {
    "name": "Changan",
    "value": 1580
  },
  {
    "name": "Changhe",
    "value": 1567
  },
  {
    "name": "Chery",
    "value": 190
  },
  {
    "name": "Chevrolet",
    "value": 13
  },
  {
    "name": "Chrysler",
    "value": 14
  },
  {
    "name": "Citroen",
    "value": 15
  },
  {
    "name": "Cupra",
    "value": 1451
  },
  {
    "name": "Dacia",
    "value": 17
  },
  {
    "name": "Dadi",
    "value": 198
  },
  {
    "name": "Daewoo",
    "value": 18
  },
  {
    "name": "DAF",
    "value": 115
  },
  {
    "name": "DAF / VDL",
    "value": 1441
  },
  {
    "name": "Dagger",
    "value": 3717
  },
  {
    "name": "Daihatsu",
    "value": 19
  },
  {
    "name": "Daimler",
    "value": 20
  },
  {
    "name": "Datsun",
    "value": 4206
  },
  {
    "name": "De Lorean",
    "value": 3071
  },
  {
    "name": "Derways",
    "value": 4328
  },
  {
    "name": "Detroit Electric",
    "value": 4883
  },
  {
    "name": "DKW",
    "value": 2243
  },
  {
    "name": "Dodge",
    "value": 118
  },
  {
    "name": "Dongfeng",
    "value": 308
  },
  {
    "name": "Dr. Motor",
    "value": 5051
  },
  {
    "name": "DS",
    "value": 4495
  },
  {
    "name": "Eagle",
    "value": 120
  },
  {
    "name": "Ernst Auwarter",
    "value": 1413
  },
  {
    "name": "Estrima",
    "value": 3921
  },
  {
    "name": "FAW",
    "value": 121
  },
  {
    "name": "Ferrari",
    "value": 22
  },
  {
    "name": "Fiat",
    "value": 23
  },
  {
    "name": "Fiat-Abarth",
    "value": 4459
  },
  {
    "name": "Fisker",
    "value": 3444
  },
  {
    "name": "Ford",
    "value": 24
  },
  {
    "name": "Fornasari",
    "value": 3104
  },
  {
    "name": "FSO",
    "value": 25
  },
  {
    "name": "FUQI",
    "value": 197
  },
  {
    "name": "Gac",
    "value": 4506
  },
  {
    "name": "Geely",
    "value": 185
  },
  {
    "name": "Genesis",
    "value": 2604
  },
  {
    "name": "Geo",
    "value": 2790
  },
  {
    "name": "GMC",
    "value": 123
  },
  {
    "name": "Golf Car",
    "value": 4316
  },
  {
    "name": "Gonow",
    "value": 183
  },
  {
    "name": "Great Wall",
    "value": 124
  },
  {
    "name": "Groz",
    "value": 1575
  },
  {
    "name": "Hafei",
    "value": 191
  },
  {
    "name": "Haima",
    "value": 3674
  },
  {
    "name": "Hanomag",
    "value": 1784
  },
  {
    "name": "Hansa",
    "value": 2053
  },
  {
    "name": "Haval",
    "value": 5456
  },
  {
    "name": "Hawtai",
    "value": 5791
  },
  {
    "name": "Hindustan",
    "value": 3411
  },
  {
    "name": "Honda",
    "value": 28
  },
  {
    "name": "Hong Xing",
    "value": 5572
  },
  {
    "name": "Horch",
    "value": 5624
  },
  {
    "name": "Huabei",
    "value": 2595
  },
  {
    "name": "Huanghai",
    "value": 388
  },
  {
    "name": "Humber",
    "value": 3002
  },
  {
    "name": "Hummer",
    "value": 127
  },
  {
    "name": "Humvee",
    "value": 4663
  },
  {
    "name": "Hyundai",
    "value": 29
  },
  {
    "name": "Infiniti",
    "value": 128
  },
  {
    "name": "Innocenti",
    "value": 4273
  },
  {
    "name": "Iran Khodro",
    "value": 3821
  },
  {
    "name": "Isuzu",
    "value": 30
  },
  {
    "name": "ItalCar",
    "value": 3757
  },
  {
    "name": "Iveco",
    "value": 175
  },
  {
    "name": "JAC",
    "value": 317
  },
  {
    "name": "Jaguar",
    "value": 31
  },
  {
    "name": "JCB",
    "value": 1590
  },
  {
    "name": "Jeep",
    "value": 32
  },
  {
    "name": "Jetour",
    "value": 55069
  },
  {
    "name": "Jiangnan",
    "value": 335
  },
  {
    "name": "Jinbei",
    "value": 2231
  },
  {
    "name": "Jinbei Minibusus",
    "value": 4549
  },
  {
    "name": "JMC",
    "value": 3018
  },
  {
    "name": "Jonway",
    "value": 1574
  },
  {
    "name": "Karosa",
    "value": 412
  },
  {
    "name": "Kia",
    "value": 33
  },
  {
    "name": "King Long",
    "value": 2676
  },
  {
    "name": "KingWoo",
    "value": 4606
  },
  {
    "name": "Kirkham",
    "value": 4843
  },
  {
    "name": "Koenigsegg",
    "value": 2643
  },
  {
    "name": "Konecranes",
    "value": 4000
  },
  {
    "name": "Lada",
    "value": 5553
  },
  {
    "name": "Lamborghini",
    "value": 35
  },
  {
    "name": "Lancia",
    "value": 36
  },
  {
    "name": "Land Rover",
    "value": 37
  },
  {
    "name": "Landwind",
    "value": 406
  },
  {
    "name": "LDV",
    "value": 134
  },
  {
    "name": "Lexus",
    "value": 38
  },
  {
    "name": "Lichi",
    "value": 5339
  },
  {
    "name": "Lifan",
    "value": 334
  },
  {
    "name": "Lincoln",
    "value": 135
  },
  {
    "name": "Lotus",
    "value": 41
  },
  {
    "name": "LTI",
    "value": 136
  },
  {
    "name": "Lucid",
    "value": 6317
  },
  {
    "name": "Luxgen",
    "value": 4269
  },
  {
    "name": "MAN",
    "value": 177
  },
  {
    "name": "Marshell",
    "value": 4064
  },
  {
    "name": "Maruti",
    "value": 139
  },
  {
    "name": "Maserati",
    "value": 45
  },
  {
    "name": "Maybach",
    "value": 46
  },
  {
    "name": "Mazda",
    "value": 47
  },
  {
    "name": "McLaren",
    "value": 3101
  },
  {
    "name": "MEGA",
    "value": 1904
  },
  {
    "name": "Mercedes-Benz",
    "value": 48
  },
  {
    "name": "Mercury",
    "value": 144
  },
  {
    "name": "Merkur",
    "value": 3948
  },
  {
    "name": "MG",
    "value": 49
  },
  {
    "name": "Microcar",
    "value": 6055
  },
  {
    "name": "Miles",
    "value": 4528
  },
  {
    "name": "MINI",
    "value": 147
  },
  {
    "name": "Mitsubishi",
    "value": 52
  },
  {
    "name": "Mitsuoka",
    "value": 402
  },
  {
    "name": "Mobility Ventures",
    "value": 4069
  },
  {
    "name": "Morgan",
    "value": 53
  },
  {
    "name": "Morris",
    "value": 54
  },
  {
    "name": "MPM Motors",
    "value": 5039
  },
  {
    "name": "MYBRO",
    "value": 5138
  },
  {
    "name": "Nissan",
    "value": 55
  },
  {
    "name": "Norster",
    "value": 2489
  },
  {
    "name": "Nysa (Ныса)",
    "value": 2045
  },
  {
    "name": "Oldsmobile",
    "value": 148
  },
  {
    "name": "Oltcit",
    "value": 2963
  },
  {
    "name": "Opel",
    "value": 56
  },
  {
    "name": "ORA",
    "value": 2974
  },
  {
    "name": "Packard",
    "value": 3193
  },
  {
    "name": "Pagani",
    "value": 2644
  },
  {
    "name": "Peerless",
    "value": 1852
  },
  {
    "name": "Peg-Perego",
    "value": 3446
  },
  {
    "name": "Peterbilt",
    "value": 346
  },
  {
    "name": "Peugeot",
    "value": 58
  },
  {
    "name": "Pininfarina",
    "value": 3590
  },
  {
    "name": "Pinzgauer",
    "value": 3215
  },
  {
    "name": "Plymouth",
    "value": 181
  },
  {
    "name": "Polestar",
    "value": 6131
  },
  {
    "name": "Pontiac",
    "value": 149
  },
  {
    "name": "Porsche",
    "value": 59
  },
  {
    "name": "Praga Baby",
    "value": 2728
  },
  {
    "name": "Proton",
    "value": 60
  },
  {
    "name": "Qifeng",
    "value": 5340
  },
  {
    "name": "Quicksilver",
    "value": 1332
  },
  {
    "name": "Ram",
    "value": 4369
  },
  {
    "name": "Ravon",
    "value": 4681
  },
  {
    "name": "Renault",
    "value": 62
  },
  {
    "name": "Renault Samsung Motors",
    "value": 4698
  },
  {
    "name": "Rezvani",
    "value": 4466
  },
  {
    "name": "Rimac",
    "value": 3330
  },
  {
    "name": "Rivian",
    "value": 6227
  },
  {
    "name": "Robeta",
    "value": 5761
  },
  {
    "name": "Roewe",
    "value": 55063
  },
  {
    "name": "Rolls-Royce",
    "value": 63
  },
  {
    "name": "Rover",
    "value": 64
  },
  {
    "name": "Saab",
    "value": 65
  },
  {
    "name": "Saipa",
    "value": 3437
  },
  {
    "name": "Saleen",
    "value": 196
  },
  {
    "name": "Samand",
    "value": 192
  },
  {
    "name": "Samson",
    "value": 3972
  },
  {
    "name": "Samsung",
    "value": 325
  },
  {
    "name": "Saturn",
    "value": 331
  },
  {
    "name": "Sceo",
    "value": 2734
  },
  {
    "name": "Scion",
    "value": 3268
  },
  {
    "name": "SEAT",
    "value": 67
  },
  {
    "name": "Secma",
    "value": 2492
  },
  {
    "name": "Selena",
    "value": 1726
  },
  {
    "name": "Shelby",
    "value": 3100
  },
  {
    "name": "Shuanghuan",
    "value": 195
  },
  {
    "name": "Sidetracker",
    "value": 4003
  },
  {
    "name": "Skoda",
    "value": 70
  },
  {
    "name": "SMA",
    "value": 311
  },
  {
    "name": "Smart",
    "value": 71
  },
  {
    "name": "SouEast",
    "value": 194
  },
  {
    "name": "Soyat",
    "value": 3212
  },
  {
    "name": "Spyker",
    "value": 411
  },
  {
    "name": "SsangYong",
    "value": 73
  },
  {
    "name": "Star",
    "value": 214
  },
  {
    "name": "Studebaker",
    "value": 3228
  },
  {
    "name": "Subaru",
    "value": 75
  },
  {
    "name": "Suda",
    "value": 2879
  },
  {
    "name": "Suda Hanen",
    "value": 55068
  },
  {
    "name": "Sunbeam",
    "value": 385
  },
  {
    "name": "Suzuki",
    "value": 76
  },
  {
    "name": "T-King",
    "value": 5341
  },
  {
    "name": "Talbot",
    "value": 77
  },
  {
    "name": "Tarpan Honker",
    "value": 2497
  },
  {
    "name": "TATA",
    "value": 78
  },
  {
    "name": "Tatra",
    "value": 204
  },
  {
    "name": "Tazzari",
    "value": 3922
  },
  {
    "name": "Tesla",
    "value": 2233
  },
  {
    "name": "Think",
    "value": 6092
  },
  {
    "name": "Think Global",
    "value": 4237
  },
  {
    "name": "Thunder Tiger",
    "value": 4033
  },
  {
    "name": "Tianma",
    "value": 1578
  },
  {
    "name": "Tiger",
    "value": 2050
  },
  {
    "name": "Tofas",
    "value": 2552
  },
  {
    "name": "Toyota",
    "value": 79
  },
  {
    "name": "Trabant",
    "value": 345
  },
  {
    "name": "Triumph",
    "value": 80
  },
  {
    "name": "TVR",
    "value": 81
  },
  {
    "name": "Ultima",
    "value": 3017
  },
  {
    "name": "Van Hool",
    "value": 206
  },
  {
    "name": "Vantage",
    "value": 5873
  },
  {
    "name": "Vauxhall",
    "value": 82
  },
  {
    "name": "Venturi",
    "value": 83
  },
  {
    "name": "Venucia",
    "value": 184
  },
  {
    "name": "Vepr",
    "value": 3320
  },
  {
    "name": "Volkswagen",
    "value": 84
  },
  {
    "name": "Volvo",
    "value": 85
  },
  {
    "name": "Wanderer",
    "value": 2021
  },
  {
    "name": "Wanfeng",
    "value": 2403
  },
  {
    "name": "Wartburg",
    "value": 339
  },
  {
    "name": "Wiesmann",
    "value": 1992
  },
  {
    "name": "Willys",
    "value": 1820
  },
  {
    "name": "Wuling",
    "value": 2653
  },
  {
    "name": "Xiaolong",
    "value": 3452
  },
  {
    "name": "Xin kai",
    "value": 338
  },
  {
    "name": "Xpeng",
    "value": 107
  },
  {
    "name": "Yogomo",
    "value": 5285
  },
  {
    "name": "Yugo",
    "value": 87
  },
  {
    "name": "Zastava",
    "value": 2309
  },
  {
    "name": "Zhidou",
    "value": 182
  },
  {
    "name": "Zimmer",
    "value": 2958
  },
  {
    "name": "Zotye",
    "value": 3610
  },
  {
    "name": "Zuk",
    "value": 3089
  },
  {
    "name": "ZX",
    "value": 322
  },
  {
    "name": "Богдан",
    "value": 188
  },
  {
    "name": "Бронто",
    "value": 3000
  },
  {
    "name": "ВАЗ",
    "value": 88
  },
  {
    "name": "ВИС",
    "value": 90
  },
  {
    "name": "ГАЗ",
    "value": 91
  },
  {
    "name": "ГолАЗ",
    "value": 410
  },
  {
    "name": "ЕРАЗ",
    "value": 170
  },
  {
    "name": "Жук",
    "value": 169
  },
  {
    "name": "ЗАЗ",
    "value": 89
  },
  {
    "name": "ЗИЛ",
    "value": 168
  },
  {
    "name": "ЗИМ",
    "value": 1544
  },
  {
    "name": "ЗИС",
    "value": 186
  },
  {
    "name": "ИЖ",
    "value": 92
  },
  {
    "name": "ЛуАЗ",
    "value": 189
  },
  {
    "name": "Москвич/АЗЛК",
    "value": 94
  },
  {
    "name": "Прицеп",
    "value": 154
  },
  {
    "name": "РАФ",
    "value": 327
  },
  {
    "name": "Ретро автомобили",
    "value": 199
  },
  {
    "name": "Самодельный",
    "value": 2863
  },
  {
    "name": "СеАЗ",
    "value": 96
  },
  {
    "name": "СМЗ",
    "value": 2491
  },
  {
    "name": "СПЭВ / SPEV",
    "value": 1351
  },
  {
    "name": "ТагАЗ",
    "value": 4537
  },
  {
    "name": "ТогАЗ",
    "value": 2638
  },
  {
    "name": "Тренер",
    "value": 4038
  },
  {
    "name": "УАЗ",
    "value": 93
  },
  {
    "name": "Циклон",
    "value": 4021
  },
  {
    "name": "Эстония",
    "value": 2307
  }
]

url_search = 'https://developers.ria.com/auto/search'
url_info = 'https://developers.ria.com/auto/info'





def get_list_car(params):
    '''
    получает словарь параметров запроса и возвращает ответ
    :param params: dict
    :return: dict
    '''
    payload = {
            'api_key': apy_key,
            'category_id': 1,

            's_yers': [2016],
            'po_yers': [2018],
            'price_ot': 10000,
            'price_do': 10500,
            'type': [
                1,  # бенз
                # 2,  # дизель
                4,   # газ
                6,  # электро
                ],
            'gearbox': [
                #1,  # механика
                2,  # автомат
                3,  # титпроник
                ],
            'countpage': 100,
            'abroad': 2,  # Не отображать авто которые находяться не в Украине
            'custom': 1,  # Не отображать нерастаможенные авто
            'with_photo': 1,  # Только с фото
            }
    payload.update(params)
    zapros_po_param = requests.get(url_search, params=payload)
    if zapros_po_param.status_code == 200:
        j = zapros_po_param.json()

        count_avto = j['result']['search_result']['count']
        list_cars = j['result']['search_result']['ids']

        return {'status': 200, 'count_avto': count_avto, 'list_cars': list_cars}
    else:
        return {'status':zapros_po_param.status_code}  # 429 (слишком много запросов)


def make_baza_avto(car_list):
    '''
    перебор списка авто для анализа
    :param car_list: list
    :return: dict
    '''
    baza_avto = {}
    for car in car_list:
        params = {
            'api_key': apy_key,
            'auto_id': car
        }
        info_avto = requests.get(url_info, params = params)
        if info_avto.status_code == 200:
            info_json = info_avto.json()
            name_avto = info_json['markName'] + ' ' + info_json['modelName']
            foto = info_json['photoData']['seoLinkB']
            price = int(info_json['USD'])
            if name_avto in baza_avto:
                #  высчитываем среднюю цену
                baza_avto[name_avto]['price'] = \
                    (baza_avto[name_avto]['count'] * baza_avto[name_avto]['price'] + price) \
                    // (baza_avto[name_avto]['count'] + 1)

                baza_avto[name_avto]['count'] += 1
            else:
                baza_avto[name_avto] = {'count': 1, 'foto': foto,  'price': price}
        else:
            return {'status': info_avto.status_code, 'baza_avto': baza_avto}
    return {'status': 200, 'baza_avto': baza_avto}



