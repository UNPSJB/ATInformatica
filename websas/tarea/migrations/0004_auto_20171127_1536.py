# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-27 15:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarea', '0003_auto_20171125_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadotarea',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'estado'), (1, 'tareapresupuestada'), (2, 'tareapendiente'), (3, 'tarearealizada'), (4, 'tareacancelada')]),
        ),
    ]
