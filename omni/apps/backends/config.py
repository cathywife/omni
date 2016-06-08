# -*- coding:utf8 -*-
"""
Created on 15-11-22 下午11:33
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function


salt_state_list = [
    {'name': 'app.restapi', 'description': 'restapi项目所有配置', 'project_name': 'restapi', 'nodegroup': ['web-restapi-01', 'web-restapi-02']},
    {'name': 'app.restapi.nginx', 'description': 'restapi项目nginx配置', 'project_name': 'restapi', 'nodegroup': ['web-restapi-01', 'web-restapi-02']},
    {'name': 'app.mainsite', 'description': '主站项目配置', 'project_name': 'mainsite',  'nodegroup': ['web-misc-01']},
    {'name': 'app.mainsite.nginx', 'description': '主站项目nginx配置', 'project_name': 'mainsite', 'nodegroup': ['web-misc-01']},
    {'name': 'app.pay', 'description': 'pay项目配置', 'project_name': 'pay', 'nodegroup': ['web-pay-01']},
    {'name': 'app.pay.nginx', 'description': 'pay项目nginx配置', 'project_name': 'pay', 'nodegroup': ['web-pay-01']},
    {'name': 'app.earthshaker', 'description': 'earthshaker项目配置', 'project_name': 'earthshaker', 'nodegroup': ['app-api-01']},
    {'name': 'app.earthshaker.nginx', 'description': 'earthshaker项目nginx配置', 'project_name': 'earthshaker', 'nodegroup': ['app-api-01']},
    {'name': 'app.web_proxy', 'description': '外卖平台接入层代理配置', 'project_name': 'web_proxy', 'nodegroup': ['web-proxy-01', 'web-proxy-02']},
    {'name': 'app.web_proxy.nginx', 'description': '外卖平台接入层代理nginx配置', 'project_name': 'web_proxy', 'nodegroup': ['web-proxy-01', 'web-proxy-02']}
]
