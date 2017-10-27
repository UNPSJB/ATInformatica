# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-25 01:57
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarifa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tarifa',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
    ]