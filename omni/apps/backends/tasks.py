# -*- coding:utf8 -*-
"""
Created on 15-12-20 下午12:13
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function


from omni.libs.saltstack.common import get_salt_master
from celery import shared_task

import logging

log = logging.getLogger(__name__)

salt_master = get_salt_master()


@shared_task(name='backends.saltstack.cmd')
def salt_master_cmd(tgt, fun, arg=(), timeout=None, expr_form='glob', ret='', jid='', kwarg=None, **kwargs):
    """
    执行saltstack模块
    :return:
    """
    # if kwarg:
    #     kwargs['kwarg'] = kwarg
    # if arg:
    #     kwargs['arg'] = arg
    # if timeout:
    #     kwargs['timeout'] = timeout
    # if expr_form:
    #     kwargs['expr_form'] = expr_form
    # if ret:
    #     kwargs['ret'] = ret
    # if jid:
    #     kwargs['jid'] = jid
    if not expr_form:
        expr_form = 'glob'

    log.info('开始调用salt-master执行操作, tgt: {0}; fun: {1}; arg: {2}; expr_form: {3}'.format(
        tgt, fun, arg if arg else '无', expr_form))
    result = salt_master.cmd(tgt, fun, arg, timeout=timeout, expr_form=expr_form, ret=ret, jid=jid, kwarg=kwarg,
                             **kwargs)
    if result:
        log.info('调用salt-master执行操作成功, 涉及节点: {0}'.format(result.keys()))
    else:
        log.error('调用salt-master执行操作失败, 没有匹配任何节点或者所有节点都没有响应')
    return result


@shared_task(name='backends.saltstack.async')
def salt_master_async(tgt, fun, arg=(), timeout=None, expr_form='glob', ret='', jid='', kwarg=None, **kwargs):
    """
    异步执行saltstack模块
    :return:
    """
    return salt_master.async(tgt, fun, arg, timeout=timeout, expr_form=expr_form, ret=ret, jid=jid, kwarg=kwarg, **kwargs)
