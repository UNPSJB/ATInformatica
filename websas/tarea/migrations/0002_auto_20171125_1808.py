# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-25 18:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tarea', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='observaciontarea',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='estadotarea',
            name='tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', to='tarea.Tarea'),
        ),
        migrations.AddField(
            model_name='estadotarea',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='tarea',
            unique_together=set([('tipo_tarea', 'orden')]),
        ),
    ]