# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 20:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('tipo_doc', models.CharField(choices=[('DU', 'DNI'), ('CL', 'CUIL'), ('CT', 'CUIT')], default='DU', max_length=2)),
                ('doc', models.CharField(max_length=20, unique=True)),
                ('domicilio', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'rol'), (1, 'tecnico'), (2, 'cliente'), (3, 'jefetaller'), (4, 'gerente'), (10, 'usuario')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='persona.Rol')),
            ],
            options={
                'abstract': False,
            },
            bases=('persona.rol',),
        ),
        migrations.CreateModel(
            name='Gerente',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='persona.Rol')),
            ],
            options={
                'abstract': False,
            },
            bases=('persona.rol',),
        ),
        migrations.CreateModel(
            name='JefeTaller',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='persona.Rol')),
            ],
            options={
                'abstract': False,
            },
            bases=('persona.rol',),
        ),
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('rol_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='persona.Rol')),
            ],
            options={
                'abstract': False,
            },
            bases=('persona.rol',),
        ),
        migrations.AddField(
            model_name='rol',
            name='persona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='persona.Persona'),
        ),
    ]
