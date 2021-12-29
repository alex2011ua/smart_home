import requests
import datetime


class DayOff:
    '''
    Ответ сервиса 	Значение 	Код возврата HTTP
    0 	Рабочий день 	200
    1 	Нерабочий день 	200
    100 	Ошибка в дате 	400
    101 	Данные не найдены 	404
    '''

    def return_dey_off(self):
        date_now = datetime.datetime.now()
        r = requests.get(f'https://isdayoff.ru/{date_now.date()}?cc=ua')
        if r.text == '0':
            print('Рабочий день')
            return False
        elif r.text == '1':
            print('Выходной')
            return True
        else:
            print(date_now.date())
            print(r.text)
            raise Exception


if __name__ == "__main__":
    a = DayOff()
    a.return_dey_off()
