# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 13:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarea', '0007_auto_20171205_1341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadotarea',
            name='deleted',
        ),
    ]
