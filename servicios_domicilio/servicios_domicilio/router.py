from rest_framework import routers 
from apps.usuarios.api import UsuarioViewSet
from apps.servicios.api import ServicioViewSet
from apps.solicitudes.api import SolicitudViewSet

# Initializarel router de DRF solo una vez
router = routers.DefaultRouter() 
# Registrar un ViewSet
router.register(prefix='usuarios', viewset=UsuarioViewSet, basename = 'usuarios')
router.register(prefix='servicios', viewset=ServicioViewSet, basename = 'servicios')
router.register(prefix='solicitudes', viewset=SolicitudViewSet, basename = 'solicitudes')

urlpatterns = router.urls