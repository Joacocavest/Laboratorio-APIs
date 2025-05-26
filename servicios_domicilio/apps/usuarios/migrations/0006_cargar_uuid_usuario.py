from django.db import migrations
import uuid

def cargar_uuids(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    for user in Usuario.objects.all():
        user.uuid = uuid.uuid4()
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_usuario_uuid'),
    ]

    operations = [
        migrations.RunPython(cargar_uuids, reverse_code=migrations.RunPython.noop),
    ]