# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-25 21:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0002_auto_20171125_1808'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='producto',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='reservastock',
            unique_together=set([]),
        ),
    ]
