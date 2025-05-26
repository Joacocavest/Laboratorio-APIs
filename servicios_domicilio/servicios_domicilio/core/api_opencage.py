import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_direccion_opencage(request):
    input_text = request.GET.get('input')
    if not input_text:
        return Response({'error': 'Falta el parámetro "input".'}, status=400)

    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {
        'q': input_text,
        'key': settings.OPENCAGE_API_KEY,
        'language': 'es',
        'limit': 3  # devuelvo hasta 3 resultados
    }

    try:
        r = requests.get(url, params=params)
        data = r.json()

        if r.status_code != 200:
            return Response({'error': data.get('status', {}).get('message', 'Error')}, status=r.status_code)

        resultados = []
        for resultado in data.get('results', []):
            resultados.append({
                'direccion_formateada': resultado.get('formatted'),
                'lat': resultado['geometry']['lat'],
                'lon': resultado['geometry']['lng'],
                'pais': resultado['components'].get('country'),
                'ciudad': resultado['components'].get('city') or resultado['components'].get('town'),
                'codigo_postal': resultado['components'].get('postcode'),
            })

        return Response(resultados)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
