from django.db import models

# Create your models here.
class contratacion(models.Model):
    ESTADO = [                             #revisar
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('finalizada', 'Finalizada')
    ]
    cliente = models.ForeignKey(
        'usuarios.Usuario', 
        related_name='contrataciones', 
        on_delete=models.CASCADE 
    )
    trabajador = models.ForeignKey(
        'usuarios.Usuario', 
        related_name='trabajos', 
        on_delete=models.CASCADE 
    )
    servicio = models.ForeignKey(
        'servicios.Servicio', 
        on_delete=models.CASCADE
    )
    direccion = models.CharField(
        max_length=250, 
        blank=False, 
        unique=True
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO, default='pendiente')

    def str(self):
        return f'{self.servicio.nombre} - {self.cliente.username} - {self.trabajador.username} - {self.estado}'