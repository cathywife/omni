# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-27 19:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(help_text=b'\xe5\x90\x8d\xe7\xa7\xb0', max_length=100, unique=True)),
                ('operation', models.CharField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c', max_length=2048)),
                ('description', models.CharField(help_text=b'\xe9\x85\x8d\xe7\xbd\xae\xe6\x8f\x8f\xe8\xbf\xb0', max_length=4096)),
                ('params', models.CharField(help_text=b'\xe5\x8f\x82\xe6\x95\xb0', max_length=4096)),
            ],
            options={
                'db_table': 'cmc_config_eoc',
            },
        ),
        migrations.CreateModel(
            name='ConfigTypeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(help_text=b'\xe9\x85\x8d\xe7\xbd\xae\xe7\xb1\xbb\xe5\x9e\x8b\xe5\x90\x8d\xe7\xa7\xb0', max_length=20, unique=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('description', models.CharField(help_text=b'\xe9\x92\x88\xe5\xaf\xb9\xe9\x85\x8d\xe7\xbd\xae\xe7\xb1\xbb\xe5\x9e\x8b\xe7\x9a\x84\xe8\xaf\xa6\xe7\xbb\x86\xe6\x8f\x8f\xe8\xbf\xb0', max_length=1024, verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0')),
            ],
            options={
                'db_table': 'cmc_config_type',
            },
        ),
        migrations.CreateModel(
            name='UserDepartmentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(help_text='\u90e8\u95e8\u540d\u79f0', max_length=50, unique=True)),
                ('visible_name', models.CharField(blank=True, help_text='\u90e8\u95e8\u663e\u793a\u540d', max_length=50, null=True)),
                ('description', models.CharField(blank=True, help_text='\u63cf\u8ff0\u3001\u8bf4\u660e\u4fe1\u606f', max_length=100, null=True)),
            ],
            options={
                'db_table': 'user_department',
            },
        ),
        migrations.CreateModel(
            name='UserGroupModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(help_text='\u7528\u6237\u7ec4,\u82f1\u6587\u5b57\u7b26/\u6570\u5b57', max_length=50, unique=True)),
                ('visible_name', models.CharField(blank=True, help_text='\u7528\u6237\u7ec4\u663e\u793a\u540d', max_length=50, null=True)),
                ('description', models.CharField(blank=True, help_text='\u63cf\u8ff0\u3001\u8bf4\u660e\u4fe1\u606f', max_length=100, null=True)),
            ],
            options={
                'db_table': 'user_group',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4')),
                ('update_time', models.DateTimeField(auto_now=True, auto_now_add=True, help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4')),
                ('name', models.CharField(help_text='\u7528\u6237\u540d,\u82f1\u6587\u5b57\u7b26/\u6570\u5b57', max_length=50, unique=True)),
                ('visible_name', models.CharField(blank=True, help_text='\u7528\u6237\u663e\u793a\u540d', max_length=50)),
                ('description', models.CharField(blank=True, help_text='\u63cf\u8ff0\u3001\u8bf4\u660e\u4fe1\u606f', max_length=100)),
                ('email', models.EmailField(blank=True, help_text='\u90ae\u4ef6\u5730\u5740', max_length=254)),
                ('department', models.ForeignKey(blank=True, help_text='\u7528\u6237\u6240\u5c5e\u90e8\u95e8', null=True, on_delete=django.db.models.deletion.CASCADE, to='cmc.UserDepartmentModel')),
                ('usergroup', models.ManyToManyField(blank=True, db_table='user_relate_usergroup', help_text='\u6240\u5c5e\u7528\u6237\u7ec4\u5217\u8868', null=True, to='cmc.UserGroupModel')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='configmodel',
            name='config_type',
            field=models.ForeignKey(db_constraint=False, help_text=b'\xe9\x80\x89\xe6\x8b\xa9\xe9\x85\x8d\xe7\xbd\xae\xe7\xb1\xbb\xe5\x9e\x8b', on_delete=django.db.models.deletion.SET_NULL, to='cmc.ConfigTypeModel', verbose_name=b'\xe9\x85\x8d\xe7\xbd\xae\xe7\xb1\xbb\xe5\x9e\x8b'),
        ),
    ]
