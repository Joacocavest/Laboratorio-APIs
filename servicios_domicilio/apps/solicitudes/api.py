from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.solicitudes.models import Solicitudes
from apps.solicitudes.serializers import SolicitudSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.usuarios.permissions import EsCliente
from .filters import SolicitudesFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, OR
from .permissions import EsClienteYDueñoSolicitud, EsTrabajadorAsignado

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudSerializer
    filter_backends= [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SolicitudesFilter
    ordering_fields= ['fecha_creacion', 'fecha_solicitada']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Solicitudes.objects.all()
        elif user.tipo == 'cliente':
            return Solicitudes.objects.filter(cliente=user)
        elif user.tipo == 'trabajador':
            return Solicitudes.objects.filter(trabajador=user)
        return Solicitudes.objects.none()

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [IsAuthenticated(), EsCliente()]  # Solo clientes pueden crear
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OR(EsClienteYDueñoSolicitud(), EsTrabajadorAsignado())]
        elif self.action in ['aceptar', 'rechazar']:
            return [IsAuthenticated(), EsTrabajadorAsignado()]
        return super().get_permissions()

    # def perform_update(self, serializer):
    #     user = self.request.user
    #     if user.tipo == 'cliente':
    #         # Cliente solo puede modificar la fecha_solicitada
    #         serializer.save(update_fields=['fecha_solicitada'])
    #     elif user.tipo == 'trabajador':
    #         # Trabajador puede modificar fecha_solicitada y estado
    #         serializer.save(update_fields=['fecha_solicitada', 'estado'])
    #     elif user.is_staff:
    #         serializer.save()

    @action(detail=True, methods=['post'])
    def aceptar(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.trabajador != request.user:
            return Response({"error": "No autorizado"}, status=403)
        solicitud.estado = 'confirmada'
        solicitud.save()
        return Response({"mensaje": "Solicitud confirmada"})

    @action(detail=True, methods=['post'])
    def rechazar(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.trabajador != request.user:
            return Response({"error": "No autorizado"}, status=403)
        solicitud.estado = 'rechazada'
        solicitud.save()
        return Response({"mensaje": "Solicitud rechazada"})
    
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
