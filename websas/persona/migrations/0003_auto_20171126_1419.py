# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-26 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0002_auto_20171125_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'rol'), (1, 'tecnico'), (2, 'cliente'), (3, 'jefetaller'), (4, 'gerente'), (10, 'usuario')]),
        ),
    ]