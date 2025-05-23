from django.urls import include, path
from servicios_domicilio import router


urlpatterns = [
    path('view-set/', include(router.urls)),
]