# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arch', '0008_auto_20161106_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectarchmodel',
            name='cluster_template',
            field=models.ManyToManyField(db_constraint=False, db_table='arch_project_arch_relate_cluster_template', help_text='\u96c6\u7fa4\u6a21\u677f', to='arch.ClusterTemplateVersionModel'),
        ),
    ]
