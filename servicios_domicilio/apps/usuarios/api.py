from rest_framework import viewsets, permissions, status, filters
from .filters import UsuarioFilter
from .models import Usuario
from .serializers import UsuarioSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


# CRUD de usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends= [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class= UsuarioFilter
    ordering_fields= ['username', 'servicio']
    # permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    # permission_classes = [IsAuthenticated, EsCliente]

    def perform_create(self, serializer):
        serializer.save()
    
    def list(self, request, *args, **kwargs):
        if request.version == '1':
            # lógica para versión 1 (podés cambiar serializer o datos)
            response = super().list(request, *args, **kwargs)
            response.data = {
                "version": "1",
                "data": response.data
            }
            return response
        elif request.version == '2':
            # lógica para versión 2 (puede incluir más info o estructura distinta)
            response = super().list(request, *args, **kwargs)
            response.data = {
                "version": "2",
                "info": "Vista extendida",
                "data": response.data
            }
            return response
        return super().list(request, *args, **kwargs)
    
class PerfilUsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)