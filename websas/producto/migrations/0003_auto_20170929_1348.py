# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-29 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_auto_20170929_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock_minimo',
            field=models.IntegerField(),
        ),
    ]
