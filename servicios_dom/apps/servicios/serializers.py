from rest_framework import serializers
from apps.servicios.models import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            'id',
            'name',
            'description'
        ]