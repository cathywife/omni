# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arch', '0002_auto_20161028_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hostmodel',
            name='hostname',
            field=models.CharField(help_text='\u4e3b\u673a\u540d', max_length=100, null=True, unique=True),
        ),
    ]