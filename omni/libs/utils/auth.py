# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年8月12日
    主要包含认证方面的方法
    用户状态说明:
    使用return_code表示用户状态代码,具体含义如下:
    0: 正常,包括：可通过认证、可登录等
    1: 认证失败,主要表示用户名、密码认证失败
    2: 用户被禁用
    3: 用户认证通过,但登录失败,原因可能与session会话创建相关
    4: 用户认证通过且成功登录
    5: 用户未登录
"""
from django.contrib import auth
status = {
    'result': True,
    'comment': '',
    'data': {},
    'return_code': 0
}


def check_user(username, password, url=None, client_ip=None):
    # 验证用户凭证
    user = auth.authenticate(username=username, password=password)
    if user:
        status['result'] = True
        status['data'] = user
        return status
    else:
        status['result'] = False
        status['return_code'] = 1
        return status


def check_session(request):
    # 验证用户session，判断用户是否已经登录
    if not request.user.is_authenticated():
        status['result'] = False
        status['return_code'] = 5
    else:
        status['result'] = True
        status['return_code'] = 4
    
    return status
