from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)
from apps.usuarios.api import PerfilUsuarioAPIView
from .core.api_google_places import buscar_direccion
from .core.api_opencage import buscar_direccion_opencage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('view-set/', include('servicios_domicilio.router')),
    path('api-view/me/', PerfilUsuarioAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/direccion/buscar/', buscar_direccion),
    path('api/direccion/buscar/', buscar_direccion_opencage),
    
]
