# -*- coding:utf8 -*-
import logging
import sys

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import auth

from omni.libs.utils.auth import check_user, check_session

log = logging.Logger(__name__)


def get_login_response(request, template_name, content):
    content.update(csrf(request))
    return render_to_response(template_name, content)


def login(request):
    """
    登录视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 登录
        username = request.POST['username']
        password = request.POST['password']
        content = dict()
        result = check_user(username, password)
        if result['result']:
            user = result['data']

            if user.is_active:
                try:
                    auth.login(request, user)
                except Exception:
                    log.error('用户"{0}"登录失败,错误信息: {1}'.format(username, sys.exc_info()))
                    content['error_msg'] = "登录失败,请重试!!"
                    return get_login_response(request, 'login.html', content)
                else:
                    return HttpResponseRedirect('/index.html')
            else:
                log.warning('用户"{0}"被锁定,但正尝试登录系统!!'.format(username))
                content['error_msg'] = '用户被锁定,禁止使用,请联系管理员解决!!'
                return get_login_response(request, 'login.html', content)
        else:
            log.debug('用户"{0}"用户名密码错误,登录失败!!'.format(username))
            content['error_msg'] = '登录失败,用户名密码错误,请重试!!'
            return get_login_response(request, 'login.html', content)
    else:
        result = check_session(request)
        if result['result']:
            return HttpResponseRedirect('/index.html')
        
        content = dict()
        content['username_length'] = 5
        content['password_length'] = 7
        content['info_msg'] = '提示: 请输入用户名及密码进行登录.'
        return get_login_response(request, 'login.html', content)


def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    auth.logout(request)
    return HttpResponseRedirect('/login.html')


def index(request):
    """
    首页
    :param request:
    :return:
    """
    from omni.page_config.navigation import aside_menu_data
    return render_to_response('index.html', {'aside_menu_data': aside_menu_data})

