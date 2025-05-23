from rest_framework import routers 
from apps.usuarios.api import UsuarioViewSet

# Initializarel router de DRF solo una vez
router = routers.DefaultRouter() 
# Registrar un ViewSet
router.register(prefix='usuarios', viewset=UsuarioViewSet, basename = 'usuarios')

urlpatterns = router.urls