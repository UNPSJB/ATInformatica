# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-24 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0006_auto_20171023_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'rol'), (2, 'cliente'), (1, 'tecnico'), (3, 'jefetaller'), (4, 'gerente'), (10, 'usuario')]),
        ),
    ]
