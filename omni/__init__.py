# -*- coding:utf8 -*-
"""
Created on 15-12-20 上午11:21
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app  # noqa
