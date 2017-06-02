# -*- coding:utf8 -*-
"""
Created on 2015年1月4日
    开发环境配置
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'omni',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': ''
    }
}

DEBUG = True


BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# CMDB
CMDB_CLIENT_ID = "3fbc37d609e64b1f81b79c7240dbb063"
CMDB_SECRET = "UTWiaxGFdnywPo1CMfeHdAcq0Cqk6VzF4GfjM2P1cyWONbsvf1q11itJAoUrQbnki8fjBEdBowTFPAk5U9hoZOd6D3fFZBUYsyFhV" \
              "A0zz1ruHhoVBuxTlKqrt2W5ayrJ"
CMDB_HOST = 'cmdb.elenet.me'
CMDB_PORT = 8080
