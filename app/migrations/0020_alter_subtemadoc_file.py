# Generated by Django 4.2.2 on 2023-09-25 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_subtemadoc_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtemadoc',
            name='file',
            field=models.FileField(upload_to='docs/'),
        ),
    ]