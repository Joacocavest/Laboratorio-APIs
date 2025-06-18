import pytest
from datetime import date, timedelta
from apps.usuarios.models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ErrorDetail
from apps.solicitudes.models import Servicio
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


#------------------------------------------------------------------------------------------------------------------------------
#       Comprobacion de las validaciones_tests


@pytest.mark.django_db
def test_no_puede_crearse_trabajador_sin_servicio(api_client):
    # Crea un superusuario administrador que puede crear otros usuarios
    admin = Usuario.objects.create_superuser(
        username="admin", email="admin@example.com", password="admin123", tipo="admin"
    )

    # Genera un token JWT de autenticación para ese admin
    refresh = RefreshToken.for_user(admin)
    token = str(refresh.access_token)

    # Asigna ese token a las cabeceras del cliente de test (para simular usuario autenticado)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Prepara los datos del nuevo trabajador, pero sin asignarle servicios (lo cual no está permitido)
    payload = {
        "username": "trabajador_sin_servicio",
        "email": "trabajador@example.com",
        "password": "testpass123",
        "tipo": "trabajador",
        "domicilio": "Don Lopez",
        "telefono": "3834568923"
        # No incluye 'servicio'
    }

    # Envía un POST a la API para intentar crear el trabajador con los datos anteriores
    response = api_client.post("/view-set/usuarios/", data=payload, format="json")
    # Espera que la API responda con un error 400 (Bad Request)
    assert response.status_code == 400
    # Verifica que el campo "servicio" esté en los errores de respuesta
    assert "servicio" in response.data
    # Verifica que el mensaje de error devuelto sea el esperado
    assert str(response.data["servicio"][0]) == "Un trabajador debe tener un servicio."
    
@pytest.mark.django_db
def test_validacion_cliente_con_servicio(api_client, servicio):
    #Test validación: cliente no debe tener servicios asignados
    # Crear un superusuario para autenticar y crear usuarios
    admin = Usuario.objects.create_superuser(
        username="admin", email="admin@example.com", password="admin123", tipo="admin"
    )

    refresh = RefreshToken.for_user(admin)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
    payload={
        "username": "cliente_con_servicio",
        "email": "cliente@example.com",
        "password": "testpass123",
        "tipo": "cliente",
        "domicilio": "Don pepe",
        "telefono": "3834568923",
        "servicio": [servicio.nombre]

    }
    
    response = api_client.post("/view-set/usuarios/", data=payload, format="json")

    print(response.data)
    assert response.status_code == 400
    assert "servicio" in response.data
    assert str(response.data["servicio"][0]) == "Un cliente no debe tener un servicio asignado."
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#       Endpoints protegidos

@pytest.mark.django_db
def test_cliente_autenticado_puede_crear_solicitud(get_authenticated_client, trabajador, servicio):

    client = get_authenticated_client

    payload = {
        "trabajador": trabajador.id,
        "servicio": servicio.id,
        "direccion": "Test 456",
        "fecha_solicitada": str(date.today() + timedelta(days=1)),
        "descripcion": "Solicitud válida"
    }

    response = client.post("/view-set/solicitudes/", data=payload, format="json")
    assert response.status_code == 201



@pytest.mark.django_db
def test_listado_solicitudes_requiere_autenticacion(api_client):
    client = api_client
    response = client.get("/view-set/solicitudes/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    

@pytest.mark.django_db
def test_trabajador_no_puede_crear_solicitud(trabajador, servicio, get_authenticated_worker):

    payload = {
        "trabajador": trabajador.id,
        "servicio": servicio.id,
        "direccion": "Calle falsa 123",
        "fecha_solicitada": str(date.today() + timedelta(days=1)),
        "descripcion": "No debería poder crear esto"
    }

    response = get_authenticated_worker.post("/view-set/solicitudes/", data=payload, format="json")
    assert response.status_code == 403  #trabajador, no es cliente ni admin
