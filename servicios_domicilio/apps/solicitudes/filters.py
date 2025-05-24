from django_filters import rest_framework as filters
from .models import Solicitudes

class SolicitudesFilter(filters.FilterSet):
    cliente = filters.CharFilter(field_name='username', lookup_expr='icontains')
    trabajador = filters.CharFilter(field_name='username', lookup_expr='icontains')
    servicio = filters.CharFilter(field_name='servicio__nombre', lookup_expr='icontains')
    fecha_creacion = filters.DateFilter(field_name='fecha_creacion', lookup_expr='date')
    fecha_solicitada = filters.DateFilter(field_name='fecha_solicitada', lookup_expr='date')

    class Meta:
        model = Solicitudes
        fields = ['cliente','trabajador','servicio','fecha_creacion','fecha_solicitada']