from django.contrib import admin
from .models import Solicitudes
from apps.solicitudes.forms import SolicitudesAdminForm

class SolicitudesAdmin(admin.ModelAdmin):
    form = SolicitudesAdminForm
    list_display = ['cliente', 'trabajador', 'servicio', 'fecha_solicitada', 'estado']
    list_filter = ['estado']
    
admin.site.register(Solicitudes)