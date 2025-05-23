from rest_framework import serializers
from apps.usuarios.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Usuario
        fields= [
            'id',
            'username',
            'tipo',
            'domicilio',
            'email',
            'servicio',
            'telefono'
        ]

        read_only_fields = [
            'id',
        ]

class RegistroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields= [
            'id',
            'username',
            'tipo',
            'domicilio',
            'email',
            'servicio',
            'telefono'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user