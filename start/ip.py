import requests


def ip_info(ip):
    print(ip)
    payload = {'ip': ip
               }
    url = 'http://ip-api.com/json/'
    r = requests.get(url, params = payload)
    d = r.json()
    return str(d)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip