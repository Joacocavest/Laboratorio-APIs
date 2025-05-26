from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
# Create your models here.

class Usuario(AbstractUser):
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    TIPO = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador')
    ]

    tipo = models.CharField(max_length=20, choices=TIPO)
    domicilio= models.CharField(max_length=250, blank=True, unique=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=10, blank=True)
    servicio = models.ForeignKey(
        'servicios.Servicio',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def clean(self):
        # Si es trabajador, servicio es obligatorio
        if self.tipo == 'trabajador' and not self.servicio:
            raise ValidationError("Un trabajador debe tener un servicio asignado.")
        # Si es cliente, servicio debe ser None
        if self.tipo == 'cliente' and self.servicio:
            raise ValidationError("Un cliente no debe tener un servicio asignado.")

    def __str__(self):
        return f'{self.username} - ({self.tipo}) - ({self.servicio})'
    
