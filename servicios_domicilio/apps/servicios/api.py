from rest_framework import viewsets, permissions
from apps.servicios.models import Servicio
from apps.servicios.serializers import ServicioSerializer

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]