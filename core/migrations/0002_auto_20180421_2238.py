# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-21 13:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='period',
            old_name='thr',
            new_name='thu',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='user',
        ),
    ]
