# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-21 14:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='period',
            name='end',
        ),
        migrations.RemoveField(
            model_name='period',
            name='fri',
        ),
        migrations.RemoveField(
            model_name='period',
            name='mon',
        ),
        migrations.RemoveField(
            model_name='period',
            name='start',
        ),
        migrations.RemoveField(
            model_name='period',
            name='thu',
        ),
        migrations.RemoveField(
            model_name='period',
            name='tue',
        ),
        migrations.RemoveField(
            model_name='period',
            name='wed',
        ),
    ]