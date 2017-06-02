# -*- coding:utf8 -*-
"""
Created on 16/9/30 下午1:25
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django import forms
from omni.libs.django.form.common import BootstrapModelForm
from omni.libs.django.form import bootstrap
from ..models.product import ProductModel, ProjectModel, AppIdModel


@bootstrap.bootstrap_form_decorator
class ProductForm(BootstrapModelForm):
    """
    产品信息Form
    """
    class Meta:
        model = ProductModel
        exclude = ('update_time', 'create_time')


@bootstrap.bootstrap_form_decorator
class ProjectForm(BootstrapModelForm):
    """
    项目信息Form
    """
    product = forms.ChoiceField(label='所属产品', help_text='选择项目所属的产品, 一个项目只能所属一个产品')
    dev_department = forms.ChoiceField(label='所属部门', help_text='选择项目的owner部门')

    class Meta:
        model = ProjectModel
        exclude = ('update_time', 'create_time')


@bootstrap.bootstrap_form_decorator
class AppIdForm(BootstrapModelForm):

    product = forms.ChoiceField(required=False, label='所属产品', help_text='选择项目所属的产品')
    project = forms.MultipleChoiceField(required=False, label='所属项目', help_text='选择AppId所属的项目')
    owner = forms.ChoiceField(required=True, label='项目Owner', help_text='项目责任人, 项目提议、立项、开发、维护人员')
    dev_department = forms.ChoiceField(required=False, label='所属部门', help_text='选择AppId的owner部门')

    class Meta:
        model = AppIdModel
        exclude = ('update_time', 'create_time', 'life_cycle')

