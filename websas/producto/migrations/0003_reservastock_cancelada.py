# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_reservastock_tarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservastock',
            name='cancelada',
            field=models.BooleanField(default=False),
        ),
    ]