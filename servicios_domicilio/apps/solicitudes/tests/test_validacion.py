import pytest
from datetime import date, timedelta
from apps.solicitudes.models import Solicitudes
from rest_framework.test import APIClient
from rest_framework import status

"""
Test de API REST para la aplicación de servicios a domicilio.

Este módulo contiene pruebas automáticas para:
- Comprobar las reglas de negocio (validaciones en usuarios y solicitudes)
- Verificar permisos y autenticación por tipo de usuario
- Simular respuestas de servicios externos (OpenCage API)
- Confirmar integridad de relaciones entre modelos

Frameworks:
- pytest
- pytest-django
- Django REST Framework
"""


#----------------------------------------------------------------------------------------------------------------------------------
#       Comprobacion de las validaciones_tests
#----------------------------------------------------------------------------------------------------------------------------------

@pytest.mark.django_db
def test_creacion_fallida_fecha_pasada(get_authenticated_client, trabajador, servicio):
    client = get_authenticated_client
    fecha_pasada = date.today() - timedelta(days=1)

    payload = {
        "trabajador": trabajador.id,
        "servicio": servicio.id,
        "direccion": "Av. Siempre Viva 742",
        "fecha_solicitada": str(fecha_pasada),
        "descripcion": "Prueba con fecha inválida"
    }

    response = client.post("/view-set/solicitudes/", data=payload, format='json')

    assert response.status_code == 400
    assert "fecha_solicitada" in response.data
    assert str(response.data["fecha_solicitada"][0]) == "La fecha de solicitud debe ser posterior a hoy."
    




@pytest.mark.django_db
def test_buscar_direccion_opencage_ok(mocker, api_client):
    # Este test verifica que el endpoint API-EXTERNA funcione correctamente
    # cuando se consulta una dirección, simulando una respuesta exitosa desde la API externa OpenCage.

    client = api_client  # Cliente no autenticado (pero DRF permite GET públicos en esta ruta)

    # Simulamos una respuesta JSON que normalmente devolvería la API de OpenCage
    fake_response_data = {
        "results": [
            {
                "formatted": "Av. Sal Gema 1635, Argentina",  # Dirección formateada
                "geometry": {"lat": -28.4946078, "lng": -65.8066178},  # Coordenadas simuladas
                "components": {
                    "country": "Argentina",
                    "city": "San Fernando del Valle de Catamarca",
                    "postcode": "null"
                }
            }
        ],
        "status": {"code": 200, "message": "OK"}  # Estado simulado de éxito
    }

    # ⚠ MOCK: Simulamos (parcheamos) la función requests.get para que no haga una llamada real.
    mock_get = mocker.patch("requests.get")  # mocker es un fixture de pytest-mock

    # Forzamos que el código de respuesta sea 200
    mock_get.return_value.status_code = 200

    # Forzamos que el contenido de la respuesta sea el JSON definido arriba
    mock_get.return_value.json.return_value = fake_response_data

    # Hacemos una llamada al endpoint de nuestra API con una dirección de prueba
    response = client.get("/api/direccion/buscar/", {"input": "Av. Sal Gema 1635"})


    # ----------------------
    # VALIDACIONES (asserts)
    # ----------------------

    # Verificamos que el código de estado sea 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Verificamos que el resultado sea una lista (como lo define la vista)
    assert isinstance(response.data, list)

    # Comprobamos que el contenido de la primera respuesta es correcto
    assert response.data[0]["direccion_formateada"] == "Av. Sal Gema 1635, Argentina"
    assert response.data[0]["pais"] == "Argentina"
    assert response.data[0]["ciudad"] == "San Fernando del Valle de Catamarca"
    assert response.data[0]["codigo_postal"] == "null"
    