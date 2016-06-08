# -*- coding:utf8 -*-
"""
Created on 16-1-4 下午9:37
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

import datetime

from omni.libs.django.view.edit import CommonCreateView
from omni.libs.django.view.list import CommonListView
from .forms import ServerAssetForm
from .models import ServerModel


class ServerAssetCreateView(CommonCreateView):

    form_class = ServerAssetForm
    template_name = 'env/index.html'

    fields_default = dict()
    fields_default['create_time'] = datetime.datetime.now()
    fields_default['update_time'] = datetime.datetime.now()


class ServerAssetListView(CommonListView):

    template_name = 'server/index.html'
    context_object_name = 'server_list_object'
    model = ServerModel

    fields_default = dict()
    fields_default['create_time'] = datetime.datetime.now()
    fields_default['update_time'] = datetime.datetime.now()

