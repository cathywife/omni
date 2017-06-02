# -*- coding:utf8 -*-
"""
Created on 16/6/9 上午10:52
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.conf import settings
from cmdblib.client import Client


cmdb_client = Client(client_id=settings.CMDB_CLIENT_ID,
                     secret=settings.CMDB_SECRET,
                     host=settings.CMDB_HOST,
                     port=settings.CMDB_PORT)


def cmdb_result_parse(result_info):
    """
    解析cmdb结果,返回统一的格式
    :param result_info:
    :return:
    """
    if len(result_info) == 3:
        result, info, task_id = result_info
        if info.get('code', 0) in [200, 304]:
            result = True
        add_result = {'result': result, 'msg': info['message'], 'http_status': info['code'], 'task_id': task_id}
    else:
        result, status, task_info, msg, task_id = result_info
        add_result = {'result': result, 'msg': msg, 'task_id': task_id}

    return add_result
