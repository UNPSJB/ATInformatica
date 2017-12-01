# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-30 21:56
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0003_orden_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='precio_final',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
    ]