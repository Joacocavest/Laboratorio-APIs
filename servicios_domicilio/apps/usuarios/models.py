from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    TIPO = [
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador')
    ]

    tipo = models.CharField(max_length=20, choices=TIPO)
    domicilio= models.CharField(max_length=250, blank=True, unique=True)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=10, blank=True)
    
    if tipo == 'trabajador':
        servicio = models.ForeignKey(
            'servicios.Servicio',
            null=False,
            blank=False,
            on_delete=models.CASCADE
        )
    else:
        servicio = models.ForeignKey(
        'servicios.Servicio',
        null=True,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return f'{self.username} - ({self.tipo})'