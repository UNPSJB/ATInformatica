# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-29 21:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarea', '0002_auto_20171029_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarea',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='tarea',
            name='repuesto',
        ),
    ]
