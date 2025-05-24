from datetime import timezone
from rest_framework import serializers
from apps.solicitudes.models import Solicitudes
from apps.servicios.models import Servicio
from apps.usuarios.models import Usuario


class SolicitudSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField(read_only=True)
    trabajador = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(tipo='trabajador'))
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())

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
    
    def validate_fecha_solicitada(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La fecha de solicitud debe ser posterior a hoy.")
        return value
    