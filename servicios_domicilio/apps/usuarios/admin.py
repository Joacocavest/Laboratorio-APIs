from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario 
from .forms import UsuarioCreationForm, UsuarioChangeForm

class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioChangeForm
    model = Usuario
    list_display = ['username', 'email', 'tipo', 'domicilio', 'telefono', 'mostrar_servicios', 'is_staff']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email', 'tipo', 'domicilio', 'telefono', 'servicio')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'tipo', 'domicilio', 'telefono', 'servicio', 'password1', 'password2'),
        }),
    )
    def mostrar_servicios(self, obj):
        return ", ".join([s.nombre for s in obj.servicios.all()])
    mostrar_servicios.short_description = 'Servicios'

admin.site.register(Usuario, UsuarioAdmin)