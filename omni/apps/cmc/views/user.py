# -*- coding:utf8 -*-
"""
Created on 16/9/28 上午11:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function


from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import filters
from omni.libs.django.view.common import MatchByUrlTemplateView

from ..models.user import UserModel, UserGroupModel, UserDepartmentModel
from ..serializers.user import UserModelSerializer, UserGroupModelSerializer, UserDepartmentModelSerializer
from ..forms.user import UserInfoForm, UserGroupForm, UserDepartmentForm
from ..filters.user import UserGroupFilterSet

import logging

log = logging.getLogger(__name__)

body_header_navigation = {'main': '用户管理', 'minor': '', 'page': ''}


class UserListCreateAPIView(ListCreateAPIView):
    """
    post: 创建一个User实例
    get: 获取user 列表
    """
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    下线、更新、检索 user对象
    """
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer


class UserGroupListCreateAPIView(ListCreateAPIView):
    """
    post: 创建一个UserGroup实例
    get: 获取user group 列表
    """
    queryset = UserGroupModel.objects.all()
    serializer_class = UserGroupModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserGroupFilterSet


class UserGroupDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    下线、更新、检索 UserGroup对象
    """
    queryset = UserGroupModel.objects.all()
    serializer_class = UserGroupModelSerializer


class UserDepartmentListCreateAPIView(ListCreateAPIView):
    """
    post: 创建一个user department实例
    get: 获取user department列表
    """
    queryset = UserDepartmentModel.objects.all()
    serializer_class = UserDepartmentModelSerializer


class UserDepartmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    下线、更新、检索user department对象
    """
    queryset = UserDepartmentModel.objects.all()
    serializer_class = UserDepartmentModelSerializer


class UserInfoCreateTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation
    body_header_navigation['minor'] = '用户'
    body_header_navigation['page'] = '创建用户'

    def get_context_data(self, **kwargs):
        context = {'form': UserInfoForm}
        kwargs.update(context)

        return super(UserInfoCreateTemplateView, self).get_context_data(**kwargs)


class UserGroupCreateTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation
    body_header_navigation['minor'] = '用户组'
    body_header_navigation['page'] = '创建用户组'

    def get_context_data(self, **kwargs):
        context = {'form': UserGroupForm}
        kwargs.update(context)

        return super(UserGroupCreateTemplateView, self).get_context_data(**kwargs)


class UserDepartmentCreateTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation
    body_header_navigation['minor'] = '部门'
    body_header_navigation['page'] = '创建部门'

    def get_context_data(self, **kwargs):
        context = {'form': UserGroupForm}
        kwargs.update(context)

        return super(UserDepartmentCreateTemplateView, self).get_context_data(**kwargs)


class UserDepartmentDetailTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation
    body_header_navigation['minor'] = '部门'
    body_header_navigation['page'] = '部门详情'

    def get_context_data(self, **kwargs):
        context = {'form': UserGroupForm}
        kwargs.update(context)

        return super(UserDepartmentDetailTemplateView, self).get_context_data(**kwargs)

