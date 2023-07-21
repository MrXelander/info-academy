# Generated by Django 4.2.2 on 2023-07-12 01:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_tema_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='tema',
            name='alumnos',
            field=models.ManyToManyField(blank=True, default='', related_name='materias_inscritas', to=settings.AUTH_USER_MODEL),
        ),
    ]
