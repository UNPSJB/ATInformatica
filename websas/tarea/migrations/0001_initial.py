# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-30 07:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rubro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'estado'), (1, 'tareapresupuestada'), (2, 'tareaesperarepuestos'), (3, 'tareapendiente'), (4, 'tarearealizada'), (5, 'tareacancelada')])),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='TipoTarea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('descripcion', models.CharField(blank=True, max_length=100, null=True)),
                ('rubro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tipos_tareas', to='rubro.Rubro')),
            ],
        ),
        migrations.CreateModel(
            name='TareaCancelada',
            fields=[
                ('estadotarea_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tarea.EstadoTarea')),
            ],
            bases=('tarea.estadotarea',),
        ),
        migrations.CreateModel(
            name='TareaEsperaRepuestos',
            fields=[
                ('estadotarea_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tarea.EstadoTarea')),
            ],
            bases=('tarea.estadotarea',),
        ),
        migrations.CreateModel(
            name='TareaPendiente',
            fields=[
                ('estadotarea_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tarea.EstadoTarea')),
            ],
            bases=('tarea.estadotarea',),
        ),
        migrations.CreateModel(
            name='TareaPresupuestada',
            fields=[
                ('estadotarea_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tarea.EstadoTarea')),
            ],
            bases=('tarea.estadotarea',),
        ),
        migrations.CreateModel(
            name='TareaRealizada',
            fields=[
                ('estadotarea_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tarea.EstadoTarea')),
            ],
            bases=('tarea.estadotarea',),
        ),
        migrations.AddField(
            model_name='tarea',
            name='tipo_tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tarea.TipoTarea'),
        ),
        migrations.AddField(
            model_name='estadotarea',
            name='tarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='estados', to='tarea.Tarea'),
        ),
    ]
