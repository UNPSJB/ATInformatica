# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-05 20:25
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servicio', '0001_initial'),
        ('tarea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarifa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('tipo_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifas', to='servicio.TipoServicio')),
                ('tipo_tarea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifas', to='tarea.TipoTarea')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tarifa',
            unique_together=set([('tipo_tarea', 'tipo_servicio')]),
        ),
    ]
