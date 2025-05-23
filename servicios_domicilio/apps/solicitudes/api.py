from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.solicitudes.models import Solicitudes
from apps.solicitudes.serializers import SolicitudSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SolicitudesFilter

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

    @action(detail=True, methods=['post'])
    def aceptar(self, request, pk=None):
        solicitud = self.get_object()
        if solicitud.trabajador != request.user:
            return Response({"error": "No autorizado"}, status=403)
        solicitud.estado = 'aceptada'
        solicitud.save()
        return Response({"mensaje": "Solicitud aceptada"})

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
