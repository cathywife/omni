# -*- coding:utf8 -*-
"""
Created on 15-6-2 下午3:20
@author: FMC

侧边栏菜单字段说明:
    name: 菜单名称
    value: 具体的显示内容
    title: 提示
    url: 超链接
    bg_img: 菜单背景图片
    before_icon: 菜单value之前的图标
    after_icon: 菜单value之后的图标
    badge: 徽章数据,父级菜单没有徽章
"""
# 样式声明
fa_angle_left = 'fa fa-angle-left pull-right'


# 仪表盘
dashboard = {'name': 'Dashboard', 'value': 'Dashboard', 'title': 'Dashboard', 'url': '/',
             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
             'sub__': None}

# 资产管理
asset_manager_menu = {'name': 'asset_manager', 'value': '资产管理', 'title': '资产管理', 'url': None, 'bg_img': None,
                      'before_icon': 'fa fa-dashboard fa-fw', 'after_icon': fa_angle_left, 'badge': None, 'sub__': list()}

asset_manager_menu['sub__'].append({'name': 'server', 'value': '服务器', 'title': '服务器', 'url': '/asset/server/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_menu['sub__'].append({'name': 'software', 'value': '软件', 'title': '软件', 'url': '/asset/software/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_menu['sub__'].append({'name': 'networks', 'value': '网络', 'title': '网络', 'url': '/asset/network/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_accessory_menu = {'name': 'accessory', 'value': '配件管理', 'title': '配件管理', 'url': '/asset/accessory/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': fa_angle_left, 'badge': None,
                             'sub__': list()}
asset_manager_accessory_menu['sub__'].append({'name': 'cpu', 'value': 'CPU', 'title': 'CPU', 'url': '/asset/accessory/cpu/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_accessory_menu['sub__'].append({'name': 'dsk', 'value': '硬盘', 'title': '硬盘', 'url': '/asset/accessory/disk/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_accessory_menu['sub__'].append({'name': 'memory', 'value': '内存', 'title': '内存', 'url': '/asset/accessory/memory/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_accessory_menu['sub__'].append({'name': 'power', 'value': '电源', 'title': '电源', 'url': '/asset/accessory/power/',
                             'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                             'sub__': None})
asset_manager_menu['sub__'].append(asset_manager_accessory_menu)

# SaltStack
salt_menu = {'name': 'host', 'value': 'SaltStack', 'title': 'SaltStack', 'url': None, 'bg_img': None,
             'before_icon': 'fa fa-dashboard fa-fw', 'after_icon': fa_angle_left, 'badge': None, 'sub__': list()}

salt_menu['sub__'].append({'name': 'salt_state_list', 'value': 'State列表', 'title': 'State列表', 'url': '/backends/',
                           'bg_img': None, 'before_icon': 'fa fa-dashboard', 'after_icon': None, 'badge': None,
                           'sub__': None})


aside_menu_data = [dashboard, asset_manager_menu, salt_menu]



# project菜单
project_menu_data = {}
