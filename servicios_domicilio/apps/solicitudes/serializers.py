from django.utils import timezone
from rest_framework import serializers
from apps.solicitudes.models import Solicitudes, Servicio
from apps.usuarios.models import Usuario
from servicios_domicilio.core.utils import obtener_coordenadas

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = [
            'id',
            'nombre',
            'descripcion',
            'activo'
        ]

        read_only_fields = [
            'id'
        ]

class SolicitudSerializer(serializers.ModelSerializer):
    # cliente = serializers.SlugRelatedField(
    #     slug_field = 'username',
    #     queryset=Usuario.objects.filter(tipo='cliente')
    # )
    # trabajador = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=Usuario.objects.filter(tipo='trabajador')
    # )
    # servicio = serializers.SlugRelatedField(
    #     slug_field='nombre',
    #     queryset=Servicio.objects.all(),
    #     allow_null=True,
    #     required=False
    # )

#----------------------------------------------------------------------------------------------------------------------------
#     Solución: Elegí una de dos cosas:
# Si el cliente siempre será el usuario autenticado, marcá cliente = serializers.HiddenField(default=serializers.CurrentUserDefault()) y dejalo en read_only_fields.
# Si lo querés editable por nombre, sacalo de read_only_fields.

# Lo mismo aplica para trabajador y servicio.
#--------------------------------------------------------------------------------------------------------------------------------    
    class Meta:
        model = Solicitudes
        fields = [
            'id',
            'uuid',
            'cliente', 
            'trabajador', 
            'servicio',
            'direccion', 
            'lat',
            'lon',
            'estado', 
            'fecha_creacion', 
            'fecha_solicitada',
            'descripcion',
            'fecha_confirmacion', 
            'fecha_rechazo',
            'fecha_finalizo'
        ]
        read_only_fields = [
            'id', 
            'fecha_creacion', 
            'cliente', 
            'trabajador',
            'servicio',
            'fecha_confirmacion', 
            'fecha_rechazo',
            'fecha_finalizo',
            'estado'
        ]

    def validate_fecha_solicitada(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("La fecha de solicitud debe ser posterior a hoy.")
        return value
    
    def validate(self, data):
        trabajador = data.get('trabajador')
        cliente = data.get('cliente')
        servicio = data.get('servicio')

        if not trabajador or not cliente or not servicio:
            return data

        if trabajador.tipo != 'trabajador':
            raise serializers.ValidationError("El usuario seleccionado no es un trabajador.")
        if cliente.tipo != 'cliente':
            raise serializers.ValidationError("El usuario seleccionado no es un cliente.")
        if servicio not in trabajador.servicio.all():
            raise serializers.ValidationError("El trabajador no ofrece el servicio seleccionado.")
        return data
    
    def update(self, instance, validated_data):
        user = self.context['request'].user #Captura al usuario autenticado que hace la peticion

        if user.tipo == 'cliente':
            validated_data = {
                key: value for key, value in validated_data.items()
                if key in ['fecha_solicitada', 'descripcion']
            }
        elif user.tipo == 'trabajador':
            validated_data = {
                key: value for key, value in validated_data.items()
                if key in ['fecha_solicitada']
            }
        #Si es admin, no filtramos nada
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        direccion = validated_data.get('direccion')
        coords = obtener_coordenadas(direccion)
        if coords:
            validated_data['lat'] = coords['lat']
            validated_data['lon'] = coords['lon']
        return super().create(validated_data)