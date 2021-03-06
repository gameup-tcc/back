# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-19 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='person',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(default='', max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='username',
            field=models.CharField(default='', max_length=50, unique=True),
        ),
    ]
