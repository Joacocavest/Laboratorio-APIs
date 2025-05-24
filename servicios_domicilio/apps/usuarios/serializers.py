from rest_framework import serializers
from apps.usuarios.models import Usuario
from apps.servicios.models import Servicio

class UsuarioSerializer(serializers.ModelSerializer):
    servicio = serializers.SlugRelatedField(
        slug_field='nombre',
        queryset=Servicio.objects.all(),
        allow_null=True,
        required=False
    )
    class Meta: 
        model= Usuario
        fields= [
            'id',
            'username',
            'tipo',
            'domicilio',
            'email',
            'servicio',
            'telefono',
        ]
        read_only_fields = [
            'id',
        ]
    def validate(self, attrs):
        tipo = attrs.get('tipo')
        servicio = attrs.get('servicio')

        if tipo == 'trabajador' and not servicio:
            raise serializers.ValidationError("Un trabajador debe tener un servicio.")
        if tipo == 'cliente' and servicio:
            raise serializers.ValidationError("Un cliente no debe tener un servicio asignado.")
    
        return attrs
    
