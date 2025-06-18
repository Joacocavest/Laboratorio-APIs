# Tests Automatizados - API Servicios a Domicilio

Este proyecto cuenta con una suite de **tests automatizados** utilizando `pytest` y `pytest-django`, que garantizan la integridad de la lógica del sistema, las reglas de validación, los permisos de acceso y el funcionamiento general de los endpoints de la API REST desarrollada con Django REST Framework.

---

## ¿Qué se testea?

### Autenticación y permisos
- Acceso restringido según el tipo de usuario (`cliente`, `trabajador`, `admin`).
- Validación de token JWT y protección de endpoints.
- Trabajadores no pueden crear solicitudes (solo clientes).

### Usuarios
- Creación de usuarios válidos por tipo (`cliente` o `trabajador`).
- Restricciones de negocio:
  - Un trabajador debe tener al menos un servicio.
  - Un cliente **no puede** tener servicios asignados.

### Solicitudes
- Creación de solicitudes válidas.
- Validación de fechas (no se aceptan solicitudes con fechas pasadas).
- Acciones personalizadas:
  - `aceptar`, `rechazar`, `finalizar` solicitud.

### API externa - Geolocalización (OpenCage)
- Mock de la API de OpenCage para evitar depender de llamadas reales.
- Validación de la respuesta formateada (dirección, ciudad, país, coordenadas).


---

## Estructura de los tests

```bash
apps/
├── usuarios/
│   └── tests/
│       ├── test_usuario.py            # Validaciones de creación de usuarios y permisos
│       └── conftest.py                # Fixtures compartidos para usuarios
│
├── solicitudes/
│   └── tests/
│       ├── test_solicitud.py         # CRUD y filtros de solicitudes
│       ├── test_validaciones.py      # Reglas de negocio específicas (fechas, roles, etc.)
```

---

## Cómo ejecutar los tests

```bash
# Recomendado: entorno virtual activo
test@pc:~$ pytest
```

Si querés ver el resumen extendido y controlar qué se ejecuta:

```bash
pytest -v --tb=short --strict-markers
```

---

## Configuración de Pytest (pytest.ini)

Archivo `pytest.ini` incluido en el proyecto:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = servicios_domicilio.settings_testing
addopts = 
    --create-db
    --tb=short
    --strict-markers
    -v

testpaths = apps
python_files = test_*.py *_tests.py
default_markers =
    unit: Pruebas unitarias
    integration: Pruebas de integración
    api: Pruebas de API REST
```

---

## Ejemplos de tests

```python
@pytest.mark.django_db
def test_cliente_autenticado_puede_crear_solicitud(get_authenticated_client, trabajador, servicio):
    """Verifica que un cliente autenticado pueda crear una solicitud válida."""
    payload = {
        "trabajador": trabajador.id,
        "servicio": servicio.id,
        "direccion": "Calle falsa 123",
        "fecha_solicitada": str(date.today() + timedelta(days=1)),
        "descripcion": "Solicitud válida"
    }
    response = get_authenticated_client.post("/view-set/solicitudes/", data=payload, format="json")
    assert response.status_code == 201
```

```python
@pytest.mark.django_db
def test_buscar_direccion_opencage_ok(mocker, api_client):
    """Simula una búsqueda de dirección utilizando un mock de OpenCage API."""
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "results": [{
            "formatted": "Av. Sal Gema 1635, Argentina",
            "geometry": {"lat": -28.49, "lng": -65.80},
            "components": {
                "country": "Argentina",
                "city": "San Fernando del Valle de Catamarca",
                "postcode": "4700"
            }
        }],
        "status": {"code": 200, "message": "OK"}
    }

    response = api_client.get("/api/direccion/buscar/", {"input": "Av. Sal Gema 1635"})
    assert response.status_code == 200
    assert response.data[0]["ciudad"] == "San Fernando del Valle de Catamarca"
```

---

## Buenas prácticas incluidas

- Uso de `fixtures` reutilizables para crear usuarios y servicios.
- Separación clara entre tests de validación, lógica de negocio y endpoints protegidos.
- Tests atómicos, claros y bien documentados con `docstring`.
- Simulación de API externa con `pytest-mock` para evitar dependencia de red.

---

## Contribución

Para agregar nuevos tests:
- Usá los fixtures definidos en `conftest.py`
- Seguí el formato `test_<nombre>.py`
- Marcá con `@pytest.mark.django_db` si accedés a la base de datos

---

## Autoría de los tests

Desarrollado por:  
**Joaquín Caviedes Estrada** – Ingeniería en Informática  
**Guillermo Espinoza** - Ingeniería en Informática
Facultad de Tecnología y Ciencias Aplicadas – UNCa

---

¡La cobertura de tests es tu red de seguridad!
Usá `pytest` para asegurarte de que tu lógica de negocio resista los cambios sin romperse.
