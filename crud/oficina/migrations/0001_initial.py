# Generated by Django 5.2.4 on 2025-07-25 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oficina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('nombre_corto', models.CharField(max_length=20, verbose_name='Nombre Corto')),
            ],
            options={
                'verbose_name': 'Oficina',
                'verbose_name_plural': 'Oficinas',
            },
        ),
    ]
