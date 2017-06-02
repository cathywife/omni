# -*- coding:utf8 -*-
"""
Created on 16-1-1 下午4:45
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function


from omni.libs.django.view.restful_api import CommonRestFulView


class TaskResultCeleryView(CommonRestFulView):
    """
    获取任务执行结果
    """
