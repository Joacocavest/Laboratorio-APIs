from uuid import uuid4
from django.utils import timezone
from django.db import models
from django.conf import settings

# Create your models here.
class Solicitudes(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    ESTADO = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('finalizada', 'Finalizada')
    ]
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='solicitudes_cliente', 
        on_delete=models.CASCADE 
    )
    trabajador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='solicitudes_trabajador', 
        on_delete=models.CASCADE 
    )
    servicio = models.ForeignKey(
        'servicios.Servicio', 
        on_delete=models.CASCADE
    )
    direccion = models.CharField(
        max_length=550, 
        blank=False
    )
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_solicitada = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')

    descripcion = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.servicio.nombre} - {self.cliente.username} - {self.trabajador.username} - {self.estado}'