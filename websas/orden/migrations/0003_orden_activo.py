# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-30 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0002_auto_20171125_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]