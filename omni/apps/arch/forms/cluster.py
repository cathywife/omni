# -*- coding:utf8 -*-
"""
Created on 16/8/23 上午10:42
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django import forms

from omni.libs.django.form.common import BootstrapModelForm
from omni.libs.django.form import bootstrap
from ..models.cluster import ClusterTemplateModel, ClusterTemplateVersionModel


@bootstrap.bootstrap_form_decorator
class ClusterTemplateForm(BootstrapModelForm):
    """
    集群模板
    """
    class Meta:
        model = ClusterTemplateModel
        fields = '__all__'


@bootstrap.bootstrap_form_decorator
class ClusterTemplateVersionForm(BootstrapModelForm):

    app_id = forms.MultipleChoiceField(required=False, label='App ID', help_text='请选择需在集群中部署的APPID列表')
    host_model = forms.ChoiceField(required=False, label='默认主机机型', help_text='请选择集群的默认机型, 可在创建集群时覆盖这里的选择.')
    # config = forms.MultipleChoiceField(label='集群配置',
    #                                    help_text='请添加应用于集群的配置')

    class Meta:
        model = ClusterTemplateVersionModel
        exclude = ['template', 'version', 'status', 'config']
