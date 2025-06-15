import pytest
from datetime import date, timedelta
from apps.solicitudes.models import Solicitudes
from rest_framework.test import APIClient
from rest_framework import status



#----------------------------------------------------------------------------------------------------------------------------------
#       Comprobacion de las validaciones_tests

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

    print(response.data)
    assert response.status_code == 400
    assert "fecha_solicitada" in response.data
    assert str(response.data["fecha_solicitada"][0]) == "La fecha de solicitud debe ser posterior a hoy."
    
    
    

@pytest.mark.django_db
def test_buscar_direccion_opencage_ok(mocker, api_client):
    client = api_client

    #Mock de la respuesta de requests.get()
    fake_response_data = {
        "results": [
            {
                "formatted": "Av. Sal Gema 1635, Argentina",
                "geometry": {"lat": -28.4946078,"lng": -65.8066178},
                "components": {
                    "country": "Argentina",
                    "city": "San Fernando del Valle de Catamarca",
                    "postcode": "null"
                }
            }
        ],
        "status": {"code": 200, "message": "OK"}
    }

    # Mock de requests.get para que devuelva esta respuesta
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = fake_response_data

    # Llamamos a la vista
    response = client.get("/api/direccion/buscar/", {"input": "Av. Sal Gema 1635"})

    
    print(f"Response Data: {response.data}")
    print(f"Response Content: {response.content}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert response.data[0]["direccion_formateada"] == "Av. Sal Gema 1635, Argentina"
    assert response.data[0]["pais"] == "Argentina"
    assert response.data[0]["ciudad"] == "San Fernando del Valle de Catamarca"
    assert response.data[0]["codigo_postal"] == "null"