# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-19 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persona', '0003_auto_20171208_2002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='doc',
            field=models.CharField(max_length=20),
        ),
    ]