# Generated by Django 4.2.2 on 2023-09-04 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_subtema_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Cuestionarios', 'Cuestionarios'), ('Proyectos', 'Proyectos'), ('Discusiones', 'Discusiones')], max_length=50)),
                ('subtema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subtema')),
            ],
        ),
        migrations.CreateModel(
            name='SubtemaDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('file', models.FileField(upload_to='')),
                ('subtema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subtema')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preg', models.CharField(max_length=100)),
                ('correcta', models.CharField(max_length=100)),
                ('opc_a', models.CharField(max_length=100)),
                ('opc_b', models.CharField(max_length=100)),
                ('opc_c', models.CharField(max_length=100)),
                ('evaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.evaluacion')),
            ],
        ),
    ]
