import pytest
from datetime import date, timedelta
from apps.usuarios.models import Usuario
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ErrorDetail
from apps.solicitudes.models import Servicio, Solicitudes
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


#---------------------------------------------------------------------------------
#                        Verificamos acción de aceptar para trabajador
#---------------------------------------------------------------------------------

@pytest.mark.django_db
def test_trabajador_puede_aceptar_solicitud(cliente, trabajador, servicio, get_authenticated_worker):
    
    worker = get_authenticated_worker
    # 1. Creamos una solicitud pendiente asociada a cliente y trabajador
    solicitud = Solicitudes.objects.create(
        cliente=cliente,
        trabajador=trabajador,
        servicio=servicio,
        direccion="Av. Siempre Viva 742",
        fecha_solicitada=date.today() + timedelta(days=1),
        descripcion="Necesito arreglos eléctricos",
        estado="pendiente"
    )

    # 2. Enviar POST al endpoint personalizado 'aceptar'
    url = f"/view-set/solicitudes/{solicitud.uuid}/aceptar/"
    response = worker.post(url)

    # 3. Verificar que se devuelve status 200 y mensaje de éxito
    assert response.status_code == 200
    assert response.data["mensaje"] == "Solicitud aceptada correctamente."

    # 4. Refrescar la instancia de la solicitud desde la base de datos
    solicitud.refresh_from_db()

    # 5. Verificar que el estado haya cambiado correctamente
    assert solicitud.estado == "aceptada"
    assert solicitud.fecha_confirmacion is not None
    assert solicitud.fecha_rechazo is None

@pytest.mark.django_db
def test_trabajador_ve_solo_sus_solicitudes(api_client, cliente, servicio):
    # Usamos el servicio del fixture y creamos dos trabajadores manualmente
    trabajador1 = Usuario.objects.create_user(
        username="trabajador_1",
        email="t1@example.com",
        password="test123",
        tipo="trabajador",
        domicilio="Calle 1"
    )
    trabajador2 = Usuario.objects.create_user(
        username="trabajador_2",
        email="t2@example.com",
        password="test123",
        tipo="trabajador",
        domicilio="Calle 2"
    )

    # Asignamos el mismo servicio a ambos trabajadores
    trabajador1.servicio.add(servicio)
    trabajador2.servicio.add(servicio)

    # Creamos una solicitud para cada trabajador
    Solicitudes.objects.create(
        cliente=cliente,
        trabajador=trabajador1,
        servicio=servicio,
        direccion="Direccion A",
        fecha_solicitada=date.today() + timedelta(days=1),
        descripcion="Solicitud para t1"
    )
    Solicitudes.objects.create(
        cliente=cliente,
        trabajador=trabajador2,
        servicio=servicio,
        direccion="Direccion B",
        fecha_solicitada=date.today() + timedelta(days=2),
        descripcion="Solicitud para t2"
    )

    # Autenticamos al trabajador1 usando JWT
    refresh = RefreshToken.for_user(trabajador1)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Llamamos al endpoint de solicitudes
    response = api_client.get("/view-set/solicitudes/")

    # Validamos respuesta exitosa
    assert response.status_code == 200
    resultados = response.data["results"]

    # Validamos que solo haya una solicitud y sea la asignada a trabajador1
    assert len(resultados) == 1
    assert resultados[0]["descripcion"] == "Solicitud para t1"
    
@pytest.mark.django_db
def test_cliente_ve_solo_trabajadores(api_client, cliente, trabajador):
    # Creamos un segundo cliente (con la misma lógica del fixture `cliente`)
    Usuario.objects.create_user(
        username="cliente_extra",
        email="cliente2@example.com",
        password="testpass123",
        tipo="cliente",
        domicilio="Calle falsa 999",
        telefono="3811122233"
    )

    # Autenticamos al cliente principal con JWT
    refresh = RefreshToken.for_user(cliente)
    token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # El cliente accede al listado de usuarios
    response = api_client.get("/view-set/usuarios/")

    # Verificamos que la respuesta sea exitosa
    assert response.status_code == 200

    # Obtenemos los datos del listado
    data = response.data["data"]

    # Verificamos que todos los elementos sean de tipo 'trabajador'
    assert all(user["tipo"] == "trabajador" for user in data)

    # Verificamos que el otro cliente creado no esté en la lista
    usernames = [user["username"] for user in data]
    assert "cliente_extra" not in usernames