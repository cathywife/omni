# -*- coding:utf8 -*-
"""
Created on 16-1-5 下午6:43
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from django.forms import ModelForm

from .models import ServerModel
from omni.libs.django.form import bootstrap


@bootstrap.bootstrap_form_decorator
class ServerAssetForm(bootstrap.BootstrapFormStyles, ModelForm):

    class Meta:
        exclude = ['create_time', 'update_time']
        model = ServerModel

