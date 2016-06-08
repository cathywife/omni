# -*- coding:utf8 -*-
"""
Created on 15-11-22 下午11:31
@author: FMC

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from omni.libs.django.view.base import CommonTemplateView
from .config import node_list, nodegroup_list


class NodeAndGroupListView(CommonTemplateView):
    """
    主机组列表视图
    """
    template_name = 'host/index.html'

    def get_context_data(self, **kwargs):
        context = {
            'node_list': node_list,
            'nodegroup_list': nodegroup_list
        }
        kwargs.update(context)
        return super(NodeAndGroupListView, self).get_context_data(**kwargs)

