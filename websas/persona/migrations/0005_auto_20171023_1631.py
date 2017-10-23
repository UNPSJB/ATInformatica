# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-23 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0004_rol_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'rol'), (2, 'cliente'), (1, 'tecnico'), (3, 'jefetaller'), (4, 'gerente')]),
        ),
    ]
