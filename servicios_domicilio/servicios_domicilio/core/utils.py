import requests
from django.conf import settings

def obtener_coordenadas(direccion):
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': direccion,
        'key': settings.OPENCAGE_API_KEY,
        'language': 'es',
        'limit': 1
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        resultado = r.json().get('results', [])[0]

        return {
            'lat': resultado['geometry']['lat'],
            'lon': resultado['geometry']['lng']
        }
    except Exception:
        return None
