from django.utils import timezone
from django.db import migrations
import uuid

def cargar_uuids(apps, schema_editor):
    Solicitudes = apps.get_model('solicitudes', 'Solicitudes')
    for solicitud in Solicitudes.objects.all():
        if not solicitud.uuid:
            solicitud.uuid = uuid.uuid4()
        if not solicitud.fecha_creacion:
            solicitud.fecha_creacion = timezone.now().date()
        solicitud.save()
    if Solicitudes.objects.values('uuid').distinct().count() != Solicitudes.objects.count():
        raise Exception("Hay UUID duplicados. Abortando migración.")

class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('solicitudes', '0008_solicitudes_uuid'),
    ]

    operations = [
        migrations.RunPython(cargar_uuids, reverse_code=migrations.RunPython.noop),
    ]

    