# -*- coding:utf8 -*-
"""
Created on 16/9/30 下午1:25
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django import forms
from omni.libs.django.form.common import BootstrapModelForm
from omni.libs.django.form import bootstrap
from ..models.user import UserModel, UserGroupModel, UserDepartmentModel


@bootstrap.bootstrap_form_decorator
class UserInfoForm(BootstrapModelForm):
    class Meta:
        model = UserModel
        fields = ['name', 'visible_name', 'description', 'usergroup', 'email', 'department']
        widgets = {
            # 'department': forms.SelectMultiple(attrs={'class': 'select2'}),
            'groups': forms.SelectMultiple(attrs={'class': 'select2'})
        }


@bootstrap.bootstrap_form_decorator
class UserGroupForm(BootstrapModelForm):
    class Meta:
        model = UserGroupModel
        fields = ['name', 'visible_name', 'description']


@bootstrap.bootstrap_form_decorator
class UserDepartmentForm(BootstrapModelForm):
    class Meta:
        model = UserDepartmentModel
        fields = ['name', 'visible_name', 'description']
