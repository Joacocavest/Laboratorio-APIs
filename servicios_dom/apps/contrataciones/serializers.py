from rest_framework import serializers
from apps.contrataciones.models import contratacion
from apps.usuarios.serializers import UsuarioSerializer
from apps.servicios.serializers import ServicioSerializer


class ContratacionCreateSerializer(serializers.ModelSerializer):
    cliente = UsuarioSerializer(read_only=True)
    trabajador = UsuarioSerializer(read_only=True)
    servicio = ServicioSerializer(read_only=True)
    class Meta:
        model = contratacion
        fields = [
            'id', 'cliente', 'trabajador', 'servicio',
            'direccion', 'estado', 'fecha'
        ]