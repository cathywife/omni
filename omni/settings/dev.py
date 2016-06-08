# -*- coding:utf8 -*-
"""
Created on 2015年1月4日
    开发环境配置
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'omni.apps.backends',
    'asset.apps.server'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'omni.urls'

WSGI_APPLICATION = 'omni.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'omni',
#         'HOST': 'dj-db-01.cuhmkfdpoevr.ap-northeast-1.rds.amazonaws.com',
#         'PORT': '3306',
#         'USER': 'fmc',
#         'PASSWORD': 'xiaofei4915'
#     }
# }

DEBUG = True


BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERY_ENABLE_UTC = True

