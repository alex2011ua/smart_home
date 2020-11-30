import requests


def ip_info(ip):
    print(ip)
    payload = {'ip': ip
               }
    url = 'https://api.2ip.ua/geo.json'
    r = requests.get(url, params = payload)
    d = r.json()
    return f'ip = {d["ip"]}, country - {d["country"]}, region - {d["region"]}, city - {d["city"]}'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip