#-*- coding:utf8 -*-
'''
    FMC 创建于 2014年8月13日
    通用视图
'''
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseServerError
from config.settings import BASE_DIR
from utils import confparser
from webschema.views.base import NavMenuMixin
#初始状态
status = {
          'result':True,
          'comment':'',
          'data':{},
          'return_code':0
          }


#导航及菜单通用视图
@login_required(login_url='/login.html')
def navigation_view(request, template_name=''):
    #获取导航数据
    result = utils.common.get_navdata()
    if result['result']:
        navdata_list = result['data']
    else:
        return HttpResponseServerError(context=b'获取导航栏数据失败！！')
    #获取导航级别
    nav_level = utils.common.get_navid_by_requrl(request.path, navdata_list)
    #获取菜单栏数据
    result = utils.common.get_navdata(*nav_level)
    if result['result']:
        menudata = result['data']
    else:
        return HttpResponseServerError(context=b'获取菜单栏数据失败,导航栏坐标ID为\"%s\"!!' % (str(nav_level)))
    return render_to_response(template_name, {'navdata_list':navdata_list,'menudata_list':menudata})