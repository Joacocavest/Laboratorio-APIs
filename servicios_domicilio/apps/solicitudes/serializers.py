from django.utils import timezone
from rest_framework import serializers
from apps.solicitudes.models import Solicitudes
from apps.servicios.models import Servicio
from apps.usuarios.models import Usuario


class SolicitudSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(
    queryset=Usuario.objects.filter(tipo='cliente')
    )
    trabajador = serializers.SlugRelatedField(
        slug_field='username',
        queryset=Usuario.objects.filter(tipo='trabajador')
    )
    # servicio = serializers.ReadOnlyField(source='trabajador.servicio.id')
    servicio = serializers.SlugRelatedField(
        slug_field='nombre',
        queryset=Servicio.objects.all(),
        allow_null=True,
        required=False
    )

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
            'estado',
            'cliente',
        ]
    
    def validate_fecha_solicitada(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("La fecha de solicitud debe ser posterior a hoy.")
        return value
    
    def validate(self, data):
        if data['trabajador'].tipo != 'trabajador':
            raise serializers.ValidationError("El usuario seleccionado no es un trabajador.")
        if data['cliente'].tipo != 'cliente':
            raise serializers.ValidationError("El usuario seleccionado no es un cliente.")
        return data
    