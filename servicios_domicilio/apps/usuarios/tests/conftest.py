#Preparacion de un fixture para tener en cuenta
# ================================================================

# @pytest.fixture
# def mi_fixture():
#     # 1. Preparación
#     objeto = {"nombre": "prueba", "valor": 123}

#     # 2. Retorno
#     return objeto

# ================================================================
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.solicitudes.models import Servicio, Solicitudes
from apps.usuarios.models import Usuario

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def cliente(db):
    return Usuario.objects.create_user(
        username="cliente_test",
        email="cliente@example.com",
        password="testpass123",
        tipo="cliente",
        domicilio="Don Satur",
        telefono="3834568923", 
    )
    
@pytest.fixture
def trabajador(db):
    return Usuario.objects.create_user(
        username="trabajador_test",
        email="trabajador@example.com",
        password="testpass123",
        tipo="trabajador",
        domicilio="Don Lopez",
        telefono="3834568923", 
    )

@pytest.fixture
def servicio(db, trabajador):
    servicio = Servicio.objects.create(
        nombre="Plomería",
        descripcion="Servicio general de plomería",
        activo=True
    )
    trabajador.servicio.add(servicio)
    return servicio

@pytest.fixture
def get_authenticated_client(cliente, api_client):

    refresh = RefreshToken.for_user(cliente)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client


@pytest.fixture
def get_authenticated_worker(trabajador, api_client):

    refresh = RefreshToken.for_user(trabajador)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client



