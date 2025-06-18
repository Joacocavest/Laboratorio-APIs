# Servicios a Domicilio - API REST

Sistema de gestión para la contratación de servicios a domicilio, que conecta a clientes con trabajadores autónomos (plomeros, electricistas, pintores, etc.) mediante una API desarrollada en Django REST Framework.

---

## Dominio del Sistema

El sistema se enmarca dentro del dominio de la **contratación de servicios a domicilio**, permitiendo la interacción entre **trabajadores autónomos** y **clientes particulares** que requieren dichos servicios. Inicialmente, se enfoca en servicios técnicos y manuales comunes (plomería, gas, electricidad, pintura, etc.), pero está pensado para escalar a otros rubros (salud, veterinaria, etc.).

---

##  Requisitos del Sistema

###  Requisitos Funcionales

#### Gestión de usuarios
- Dos tipos de usuarios: **Cliente** y **Trabajador**.
- Registro con formulario personalizado (nombre, domicilio, servicio, etc.).
- Los trabajadores deben indicar el servicio que ofrecen.
- Los clientes deben indicar su domicilio.

#### Autenticación y autorización
- Autenticación mediante **JSON Web Token (JWT)**.
- Solo usuarios autenticados pueden acceder a operaciones sensibles.
- Permisos basados en el tipo de usuario (cliente, trabajador, admin).

#### Gestión de servicios
- Modelo Servicio: plomería, gas, electricidad, etc.
- Los administradores pueden crear, actualizar y eliminar servicios.

#### Búsqueda de trabajadores
- Filtros disponibles:
  - Por nombre de usuario.
  - Por tipo de servicio.

#### Solicitudes de servicios
- Un cliente puede enviar una solicitud a un trabajador, indicando:
  - Fecha deseada (fecha_solicitada)
  - Dirección y descripción del problema.
- Un trabajador puede **aceptar** o **rechazar** una solicitud mediante endpoints personalizados.

#### Historial de solicitudes
- Los usuarios pueden visualizar sus solicitudes filtradas por estado:
  - pendiente, aceptada, rechazada, finalizada.

#### Consumo de API externa
- Se utiliza la API **OpenCage** para geolocalización a partir de direcciones.

---

## Modelos principales

### Usuario (Usuario)
Hereda de AbstractUser y se le agregan:
- tipo: cliente o trabajador.
- domicilio, lat, lon, telefono, email.
- servicio: FK a Servicio (solo para trabajadores).

### Servicio (Servicio)
- nombre: nombre del servicio (único).
- descripcion: texto libre.
- activo: booleano para activar o desactivar el servicio.

### Solicitudes (Solicitudes)
- cliente: FK a Usuario (tipo = cliente).
- trabajador: FK a Usuario (tipo = trabajador).
- servicio: FK a Servicio.
- estado: pendiente, aceptada, rechazada, finalizada.
- Campos automáticos: fecha_creacion, fecha_confirmacion, fecha_rechazo, fecha_finalizo.
- Campos de ubicación: direccion, lat, lon.
- Campo libre: descripcion.

---

## Permisos Personalizados

- EsCliente
- EsTrabajadorAsignado
- EsClienteYDueñoSolicitud
- EsAdministrador

---

## Endpoints Extra

### Aceptar solicitud (trabajador)
http
POST /api/solicitudes/<uuid>/aceptar/
Authorization: Bearer <token>


### Rechazar solicitud (trabajador)
http
POST /api/solicitudes/<uuid>/rechazar/
Authorization: Bearer <token>


### Finalizar solicitud (trabajador)
http
POST /api/solicitudes/<uuid>/finalizar/
Authorization: Bearer <token>


---

## Tecnologías

- **Backend:** Django 4+, Django REST Framework
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Base de datos:** SQLite (para desarrollo)
- **Geolocalización:** OpenCage API

---

## Instalación y ejecución

bash
git clone https://github.com/usuario/proyecto-servicios.git
cd servicios_domicilio
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver


SuperUser creado --> username: admin ; password: woney123#

---

## Documentación

- Todos los endpoints fueron documentados en la carpeta Postman.
- Archivo .json incluido en el repositorio para importar la colección.

---
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

## Autor

Proyecto desarrollado por Espinoza Guillermo y Caviedes Estrada Joaquin para la materia **APIs**.
