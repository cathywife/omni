# -*- coding:utf8 -*-
"""
Created on 16/10/21 下午9:08
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omni.settings')

from django.conf import settings  # noqa

app = Celery('omni')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
