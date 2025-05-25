from django import forms
from apps.solicitudes.models import Solicitudes
from apps.usuarios.models import Usuario
from apps.servicios.models import Servicio
from django.core.exceptions import ValidationError

class SolicitudesAdminForm(forms.ModelForm):
    class Meta:
        model = Solicitudes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SolicitudesAdminForm, self).__init__(*args, **kwargs)

        # Mostrar solo clientes
        self.fields['cliente'].queryset = Usuario.objects.filter(tipo='cliente')

        # Mostrar solo trabajadores
        self.fields['trabajador'].queryset = Usuario.objects.filter(tipo='trabajador')

        # Inicializar servicio vacío por defecto
        self.fields['servicio'].queryset = Servicio.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        trabajador = cleaned_data.get('trabajador')
        servicio = cleaned_data.get('servicio')

        if cliente and cliente.tipo != 'cliente':
            raise ValidationError({'cliente': 'El usuario seleccionado no es un cliente.'})

        if trabajador and trabajador.tipo != 'trabajador':
            raise ValidationError({'trabajador': 'El usuario seleccionado no es un trabajador.'})

        if trabajador and trabajador.servicio != servicio:
            raise ValidationError({'servicio': f'El trabajador seleccionado solo brinda el servicio: {trabajador.servicio}.'})

        return cleaned_data
