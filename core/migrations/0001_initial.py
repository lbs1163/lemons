# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-21 12:33

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.CharField(max_length=70)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('mon', models.BooleanField()),
                ('tue', models.BooleanField()),
                ('wed', models.BooleanField()),
                ('thr', models.BooleanField()),
                ('fri', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('code', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('code', models.CharField(max_length=40)),
                ('plan', models.TextField()),
                ('professor', models.CharField(max_length=40)),
                ('class_number', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('credit', models.CharField(max_length=40)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Category')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Semester')),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Semester')),
                ('subjects', models.ManyToManyField(to='core.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='period',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Subject'),
        ),
        migrations.AddField(
            model_name='alias',
            name='original',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Subject'),
        ),
    ]