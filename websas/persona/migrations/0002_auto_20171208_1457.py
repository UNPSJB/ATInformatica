# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-08 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Rol'), (1, 'Técnico'), (2, 'Cliente'), (3, 'Jefe de Taller'), (4, 'Gerente'), (10, 'Usuario')]),
        ),
    ]
