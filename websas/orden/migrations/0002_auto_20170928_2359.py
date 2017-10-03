# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-28 23:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rubro', '0001_initial'),
        ('servicio', '0001_initial'),
        ('persona', '0003_auto_20170914_1929'),
        ('orden', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='rubro',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rubro.Rubro'),
        ),
        migrations.AddField(
            model_name='orden',
            name='tecnico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.Tecnico'),
        ),
        migrations.AddField(
            model_name='orden',
            name='tipo_servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='servicio.TipoServicio'),
        ),
    ]