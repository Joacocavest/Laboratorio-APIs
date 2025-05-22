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
    servicio = models.ForeignKey(
        'servicios.Servicio',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def str(self):
        return f'{self.username} - ({self.tipo})'