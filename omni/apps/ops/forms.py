# -*- coding:utf8 -*-
"""
Created on 16-1-1 下午4:13
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django import forms
from django.utils.translation import ugettext_lazy as _


class TaskResultCeleryForm(forms.Form):
    """
    获取、更新Celery 任务执行结果Form
    """
    id = forms.CharField(max_length=36, min_length=36, required=True, help_text='任务ID')

