from rest_framework import serializers
from apps.usuarios.models import Usuario
from apps.solicitudes.models import Servicio
from servicios_domicilio.core.utils import obtener_coordenadas

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    servicio = serializers.SlugRelatedField(
        slug_field='nombre',
        queryset=Servicio.objects.all(),
        allow_null=True,
        required=False,
        many=True
    )

    class Meta: 
        model= Usuario
        fields= [
            'uuid',
            'username',
            'password',
            'tipo',
            'domicilio',
            'lat',
            'lon',
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
            raise serializers.ValidationError({
                "servicio": "Un trabajador debe tener un servicio."})
        if tipo == 'cliente' and servicio:
            raise serializers.ValidationError({
                "servicio": "Un cliente no debe tener un servicio asignado."
            })

    
        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        servicios = validated_data.pop('servicio', [])  # ahora es una lista
        domicilio = validated_data.get('domicilio')
        coords = obtener_coordenadas(domicilio)
        if coords:
            validated_data['lat'] = coords['lat']
            validated_data['lon'] = coords['lon']

        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()

        if servicios:
            user.servicio.set(servicios)

        return user
