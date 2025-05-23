from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.solicitudes.models import Solicitudes
from apps.solicitudes.serializers import SolicitudSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    serializer_class = SolicitudSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.tipo == 'cliente':
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