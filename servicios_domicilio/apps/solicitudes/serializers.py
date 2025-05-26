from django.utils import timezone
from rest_framework import serializers
from apps.solicitudes.models import Solicitudes
from apps.servicios.models import Servicio
from apps.usuarios.models import Usuario


class SolicitudSerializer(serializers.ModelSerializer):
    cliente = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset=Usuario.objects.filter(tipo='cliente')
    )
    trabajador = serializers.SlugRelatedField(
        slug_field='username',
        queryset=Usuario.objects.filter(tipo='trabajador')
    )
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
            'cliente',
            'trabajador',
            'servicio',
            'descripcion'
        ]
    
    def validate_fecha_solicitada(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("La fecha de solicitud debe ser posterior a hoy.")
        return value
    
    def validate(self, data):
        if self.instance is None:
            if data['trabajador'].tipo != 'trabajador':
                raise serializers.ValidationError("El usuario seleccionado no es un trabajador.")
            if data['cliente'].tipo != 'cliente':
                raise serializers.ValidationError("El usuario seleccionado no es un cliente.")
        return data
    
    def update(self, instance, validated_data):
        user = self.context['request'].user #Captura al usuario autenticado que hace la peticion

        if user.tipo == 'cliente':
            validated_data = {
                key: value for key, value in validated_data.items()
                if key == 'fecha_solicitada'
            }
        elif user.tipo == 'trabajador':
            validated_data = {
                key: value for key, value in validated_data.items()
                if key in ['fecha_solicitada', 'estado']
            }
        #Si es admin, no filtramos nada
        return super().update(instance, validated_data)