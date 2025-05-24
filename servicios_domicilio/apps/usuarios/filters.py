from django_filters import rest_framework as filters
from .models import Usuario

class UsuarioFilter(filters.FilterSet):
    nombre = filters.CharFilter(field_name='username', lookup_expr='icontains')
    servicio = filters.CharFilter(field_name='servicio__nombre', lookup_expr='icontains')

    class Meta:
        model = Usuario
        fields = ['username','servicio','tipo']
