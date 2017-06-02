# -*- coding:utf8 -*-
"""
Created on 16/9/28 上午11:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals


from ..models.product import AppIdModel, ProductModel, ProjectModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseServerError
from ..serializers.product import ProductModelSerializer, ProjectModelSerializer, AppIdModelSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, ListAPIView
from rest_framework import filters
from omni.libs.django.view.common import MatchByUrlTemplateView
from ..forms.product import ProductForm, ProjectForm, AppIdForm
from ..filters.product import ProductFilterSet, AppIdFilterSet
from omni.apps.cmc.models.user import UserDepartmentModel


import requests
import logging

log = logging.getLogger(__name__)


body_header_navigation = {'main': '产品管理', 'minor': '', 'page': ''}


class AppIdInfoUpdateAPIView(APIView):
    """
    从'http://pms.elenet.me/pmo.api/module/syncall'获取所有APPID信息,并一次性更新至DB中
    """
    @staticmethod
    def get_appid_info_from_pms():
        """
        从pms系统中获取APPID信息
        :return:
        """
        get_appid_url = 'http://pms.elenet.me/pmo.api/module/syncall'
        response_obj = requests.get(get_appid_url, timeout=3)
        if response_obj.status_code == 200:
            appid_data = response_obj.json().get('resultMsg', [])
        else:
            appid_data = []

        if not appid_data:
            return HttpResponseServerError('从PMS: "http://pms.elenet.me/pmo.api/module/syncall"获取APPID数据为空!!')

        return appid_data

    def post(self, request, *args, **kwargs):
        """
        写入db,并响应用户
        :param request:
        :param format:
        :return:
        """
        appid_info_list = self.get_appid_info_from_pms()
        change_list = {'app_id': [], 'department': []}
        for appid_info in appid_info_list:
            department_obj_data = {'name': appid_info.get('organizationName'),
                                   'visible_name': appid_info.get('departmentName')}
            user_department_obj, created = UserDepartmentModel.objects.update_or_create(
                **department_obj_data)
            if created:
                change_list['department'].append(department_obj_data)

            appid_obj_data = {
                    'name': appid_info.get('appId'),
                    # 'owner': appid_info.get('moduleOwner'),
                    'dev_department_id': user_department_obj.id
                }

            appid_info_obj, created = AppIdModel.objects.update_or_create(**appid_obj_data)
            if created:
                change_list['app_id'].append(appid_obj_data)

        log.info('从PMS: "http://pms.elenet.me/pmo.api/module/syncall"获取APPID数据成功! 共新增"{0}"个AppID, "{1}"个部门'.format(
            len(change_list['app_id']), len(change_list['department'])))
        return Response(data={'msg': 'AppID and UserDepartment already update success', 'changed_list': change_list},
                        status=status.HTTP_200_OK)


class AppIdListAPIView(ListAPIView):
    """
    get: 获取appid列表
    """
    queryset = AppIdModel.objects.select_related('dev_department').all()
    serializer_class = AppIdModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = AppIdFilterSet


class AppIdDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    下线、更新、检索 appid对象
    """
    queryset = AppIdModel.objects.all()
    serializer_class = AppIdModelSerializer


class ProductListCreateAPIView(ListCreateAPIView):
    """
    post: 创建一个ProductInfo实例
    get: 获取product 列表
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilterSet


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    下线、更新、检索 product对象
    """
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer


class ProjectListCreateAPIView(ListCreateAPIView):
    """
    post: 创建一个ProjectInfo实例
    get: 获取project列表
    """
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectModelSerializer


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    下线、更新、检索project对象
    """
    queryset = ProjectModel.objects.all()
    serializer_class = ProjectModelSerializer


class ProductCreateTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = '产品'
        self.body_header_navigation['page'] = '创建产品'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'form': ProductForm}
        kwargs.update(context)

        return super(ProductCreateTemplateView, self).get_context_data(**kwargs)


class ProjectCreateTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = '项目'
        self.body_header_navigation['page'] = '创建项目'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'form': ProjectForm}
        kwargs.update(context)

        return super(ProjectCreateTemplateView, self).get_context_data(**kwargs)


class AppIdListTemplateView(MatchByUrlTemplateView):

    template_name = 'arch/appids/list.html'

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = 'AppID'
        self.body_header_navigation['page'] = 'AppID列表'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'table_name': 'AppIdList'}
        kwargs.update(context)

        return super(AppIdListTemplateView, self).get_context_data(**kwargs)


class AppIdUpdateTemplateView(MatchByUrlTemplateView):

    template_name = 'arch/appids/update.html'

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = 'AppID'
        self.body_header_navigation['page'] = '编辑AppID'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        AppIdForm.base_fields['name'].disabled = True
        context = {'form': AppIdForm}
        kwargs.update(context)

        return super(AppIdUpdateTemplateView, self).get_context_data(**kwargs)


class AppIdDetailTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = 'AppID'
        self.body_header_navigation['page'] = 'AppID详情'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        AppIdForm.base_fields['name'].disabled = True
        context = {'form': AppIdForm}
        kwargs.update(context)

        return super(AppIdDetailTemplateView, self).get_context_data(**kwargs)


