# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-22 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0003_auto_20170914_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='tipo',
            field=models.PositiveSmallIntegerField(choices=[(0, 'rol')], default=0),
            preserve_default=False,
        ),
    ]
