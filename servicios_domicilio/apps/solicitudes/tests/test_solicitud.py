import pytest
from datetime import date, timedelta
from apps.solicitudes.models import Solicitudes

"""
Test de API REST para la aplicación de servicios a domicilio.

Este módulo contiene pruebas automáticas para:
- Validar operaciones CRUD sobre solicitudes
- Comprobar las reglas de negocio (validaciones en usuarios y solicitudes)
- Verificar permisos y autenticación por tipo de usuario
- Confirmar integridad de relaciones entre modelos

Frameworks:
- pytest
- pytest-django
- Django REST Framework
"""


@pytest.mark.django_db
def test_creacion_exitosa_solicitud(get_authenticated_client, trabajador, servicio):
    client = get_authenticated_client
    fecha_futura = date.today() + timedelta(days=1)

    payload = {
        "trabajador": trabajador.id,
        "servicio": servicio.id,
        "direccion": "Av. Siempre Viva 742",
        "fecha_solicitada": str(fecha_futura),
        "descripcion": "Necesito arreglar una cañería rota"
    }

    response = client.post('/view-set/solicitudes/', data=payload, format='json')
    
    assert response.status_code == 201
    data = response.data

    assert data["direccion"] == payload["direccion"]
    assert data["descripcion"] == payload["descripcion"]
    assert data["estado"] == "pendiente"
    assert data["servicio"] == servicio.id
    assert data["trabajador"] == trabajador.id
    assert data["fecha_solicitada"] == str(fecha_futura)

    # Verificamos en base de datos también
    assert Solicitudes.objects.filter(uuid=data["uuid"]).exists()



@pytest.mark.django_db
def test_lectura_lista_solicitudes(get_authenticated_client, cliente, trabajador, servicio):
    from apps.solicitudes.models import Solicitudes
    from datetime import date, timedelta

    solicitud = Solicitudes.objects.create(
        cliente=cliente,
        trabajador=trabajador,
        servicio=servicio,
        direccion="Prueba",
        fecha_solicitada=date.today() + timedelta(days=2),
        descripcion="desc"
    )

    client = get_authenticated_client
    response = client.get("/view-set/solicitudes/")

    assert response.status_code == 200
    print(len(response.data["data"]))
    print(response.data["data"])
    assert len(response.data["data"]) >= 1
    assert str(item["uuid"] == str(solicitud.uuid) for item in response.data["data"])


@pytest.mark.django_db
def test_update_fecha_solicitada_por_cliente(get_authenticated_client, cliente, trabajador, servicio):
    from apps.solicitudes.models import Solicitudes
    from datetime import date, timedelta

    solicitud = Solicitudes.objects.create(
        cliente=cliente,
        trabajador=trabajador,
        servicio=servicio,
        direccion="Original",
        fecha_solicitada=date.today() + timedelta(days=2),
        descripcion="Texto original"
    )

    nueva_fecha = date.today() + timedelta(days=5)

    response = get_authenticated_client.patch(
        f"/view-set/solicitudes/{solicitud.uuid}/",
        data={"fecha_solicitada": str(nueva_fecha)},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["fecha_solicitada"] == str(nueva_fecha)


@pytest.mark.django_db
def test_eliminar_solicitud_por_cliente(get_authenticated_client, cliente, trabajador, servicio):
    from apps.solicitudes.models import Solicitudes
    from datetime import date, timedelta

    solicitud = Solicitudes.objects.create(
        cliente=cliente,
        trabajador=trabajador,
        servicio=servicio,
        direccion="Original",
        fecha_solicitada=date.today() + timedelta(days=2),
        descripcion="Texto original"
    )

    response = get_authenticated_client.delete(f"/view-set/solicitudes/{solicitud.uuid}/")

    assert response.status_code == 204
    assert not Solicitudes.objects.filter(uuid=solicitud.uuid).exists()
