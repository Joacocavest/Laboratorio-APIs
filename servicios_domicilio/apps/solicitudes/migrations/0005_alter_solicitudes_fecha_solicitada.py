# Generated by Django 5.2 on 2025-05-24 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0004_alter_solicitudes_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudes',
            name='fecha_solicitada',
            field=models.DateField(),
        ),
    ]
