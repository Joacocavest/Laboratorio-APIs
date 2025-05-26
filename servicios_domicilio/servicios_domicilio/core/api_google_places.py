import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_direccion(request):
    input_text = request.GET.get('input')
    if not input_text:
        return Response({'error': 'Falta el parámetro "input".'}, status=400)

    url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
    params = {
        'input': input_text,
        'key': settings.GOOGLE_MAPS_API_KEY,
        'language': 'es',
        'types': 'address'
    }

    r = requests.get(url, params=params)
    return Response(r.json())