from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.solicitudes.models import Solicitudes, Servicio
from apps.solicitudes.serializers import SolicitudSerializer, ServicioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.usuarios.permissions import EsCliente, EsAdmin
from .filters import SolicitudesFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, OR
from .permissions import EsClienteYDueñoSolicitud, EsTrabajadorAsignado, EsAdministrador
from django.utils import timezone
from rest_framework import viewsets, permissions

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]  # todos los logueados pueden ver
        else:
            return [permissions.IsAdminUser()]  # solo admins pueden modificar

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
    
class SolicitudViewSet(viewsets.ModelViewSet):
    
    serializer_class = SolicitudSerializer
    filter_backends= [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = SolicitudesFilter
    ordering_fields= ['fecha_creacion', 'fecha_solicitada']
    lookup_field = 'uuid'
    
    

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Solicitudes.objects.all().order_by('-fecha_creacion')
        elif user.tipo == 'cliente':
            return Solicitudes.objects.filter(cliente=user).order_by('-fecha_creacion')
        elif user.tipo == 'trabajador':
            return Solicitudes.objects.filter(trabajador=user).order_by('-fecha_creacion')
        return Solicitudes.objects.none()

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [IsAuthenticated(), OR(EsCliente(), EsAdmin())]  # Solo clientes pueden crear
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), OR(OR(EsClienteYDueñoSolicitud(), EsTrabajadorAsignado()), EsAdministrador())]
        elif self.action in ['aceptar', 'rechazar', 'finalizar']:
            return [IsAuthenticated(), EsTrabajadorAsignado()]
        return super().get_permissions()
    
    @action(detail=True, methods=['post'])
    def aceptar(self, request, uuid=None):
        solicitud = self.get_object()
        if solicitud.estado != 'pendiente':
            return Response({"error": "Solo se pueden aceptar solicitudes pendientes."}, status=400)
        solicitud.estado = 'aceptada'
        solicitud.fecha_confirmacion = timezone.now()
        solicitud.fecha_rechazo = None
        solicitud.save()
        return Response({"mensaje": "Solicitud aceptada correctamente."}, status=200)

    @action(detail=True, methods=['post'])
    def rechazar(self, request, uuid=None):
        solicitud = self.get_object()
        if solicitud.estado != 'pendiente':
            return Response({"error": "Solo se pueden rechazar solicitudes pendientes."}, status=400)
        solicitud.estado = 'rechazada'
        solicitud.fecha_rechazo = timezone.now()
        solicitud.fecha_confirmacion = None
        solicitud.fecha_finalizo = None
        solicitud.save()
        return Response({"mensaje": "Solicitud rechazada correctamente."}, status=200)
    
    @action(detail=True, methods=['post'])
    def finalizar(self, request, uuid=None):
        solicitud = self.get_object()
        if solicitud.estado != 'aceptada':
            return Response({"error": "Solo se pueden finalizar solicitudes aceptadas."}, status=400)
        solicitud.estado = 'finalizada'
        solicitud.fecha_finalizo = timezone.now()
        solicitud.fecha_rechazo = None
        solicitud.save()
        return Response({"mensaje": "Solicitud finalizada correctamente."}, status=200)
        
    def list(self, request, *args, **kwargs):
        if request.version == '1':
            # lógica para versión 1 
            response = super().list(request, *args, **kwargs)
            response.data = {
                "version": "1",
                "data": response.data
            }
            return response
        elif request.version == '2':
            # lógica para versión 2
            response = super().list(request, *args, **kwargs)
            response.data = {
                "version": "2",
                "info": "Vista extendida",
                "data": response.data
            }
            return response
        return super().list(request, *args, **kwargs)
