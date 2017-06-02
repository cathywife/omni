# -*- coding:utf8 -*-
"""
Created on 16/8/23 上午10:42
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django import forms


class HostGroupRlAppidForm(forms.Form):
    """
    Appid与hostgroup的映射Form
    """
    app_id = forms.CharField(max_length=30, min_length=5)
    hostgroup_name = forms.CharField(max_length=50, min_length=5)


class HostGroupRlHostsForm(forms.Form):
    """
    HostgroupForm
    """
    hosts = forms.CharField(max_length=102400, min_length=5)
    hostgroup_name = forms.CharField(max_length=50, min_length=5)

