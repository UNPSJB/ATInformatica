# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-23 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0005_auto_20171023_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rol',
            name='persona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='persona.Persona'),
        ),
    ]
