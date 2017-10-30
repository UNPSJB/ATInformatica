# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-30 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tarea', '0002_estadotarea_usuario'),
        ('orden', '0002_auto_20171030_0724'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estado',
            name='tareas',
        ),
        migrations.AddField(
            model_name='estado',
            name='tareas',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='tarea.Tarea'),
            preserve_default=False,
        ),
    ]
