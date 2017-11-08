# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-07 23:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tarea', '0006_auto_20171103_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservacionTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('contenido', models.TextField()),
                ('tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observaciones', to='tarea.Tarea')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]