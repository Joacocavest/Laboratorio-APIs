from rest_framework import serializers
from apps.solicitudes.models import Solicitudes
from apps.usuarios.serializers import UsuarioSerializer
from apps.servicios.serializers import ServicioSerializer
from apps.servicios.models import Servicio
from apps.usuarios.models import Usuario


class SolicitudesCreateSerializer(serializers.ModelSerializer):
    cliente = UsuarioSerializer.StringRelatedField(read_only=True)
    trabajador = UsuarioSerializer.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(rol='trabajador'))
    servicio = ServicioSerializer.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    # cliente = UsuarioSerializer(read_only=True)
    # trabajador = UsuarioSerializer(read_only=True)
    # servicio = ServicioSerializer(read_only=True)
    class Meta:
        model = Solicitudes
        fields = [
            'id', 'cliente', 'trabajador', 'servicio',
            'direccion', 'estado', 'fecha_creacion', 'fecha_solicitada',
            'descripcion'
        ]

        read_only_fields = [
            'id',
            'fecha_creacion',
            'fecha_solicitada',
            'estado',
            'cliente',
        ]