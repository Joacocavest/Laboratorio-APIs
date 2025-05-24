from rest_framework import viewsets, permissions, status, filters
from .filters import UsuarioFilter
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


# CRUD de usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends= [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class= UsuarioFilter
    ordering_fields= ['username', 'servicio']
    #permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    


    