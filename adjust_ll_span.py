import requests


API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def adjust_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return None, None
    convert = toponym["boundedBy"]["Envelope"]
    left, bottom = convert["lowerCorner"].split()
    right, top = convert["upperCorner"].split()
    width = abs(float(left) - float(right))
    height = abs(float(top) - float(bottom))
    return ",".join(toponym["Point"]["pos"].split()), f"{width/2},{height/2}"


def geocode(address):
    request = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}
    response = requests.get(request, params=params)
    if response:
        jsresponse = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса:
            {request} \nHttp статус: {response.status_code} ({response.reason})""")
    features = jsresponse["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    if features:
        return features
