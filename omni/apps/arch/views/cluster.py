# -*- coding:utf8 -*-
"""
Created on 16/9/28 上午11:07
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, \
    unicode_literals

from django.db import models
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters, response, status
from omni.libs.django.view.common import MatchByUrlTemplateView

from ..models.cluster import ClusterTemplateModel, ClusterTemplateVersionModel, ClusterTemplateVersionStatusModel
from ..serializers.cluster import ClusterTemplateModeSerializer, ClusterTemplateVersionModeSerializer
from ..forms.cluster import ClusterTemplateVersionForm, ClusterTemplateForm
from ..filters.cluster import ClusterTemplateVersionFilterSet


body_header_navigation = {'main': '集群管理', 'minor': '', 'page': ''}


class ClusterTemplateListCreateAPIView(ListCreateAPIView):
    """
    集群模板的restful API create view
    """
    queryset = ClusterTemplateModel.objects.all()
    serializer_class = ClusterTemplateModeSerializer


class ClusterTemplateDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    集群模板的详情视图, get、post、put、delete
    """
    queryset = ClusterTemplateModel.objects.all()
    serializer_class = ClusterTemplateModeSerializer


class ClusterTemplateVersionListCreateAPIView(ListCreateAPIView):
    """
    集群模板版本的restful API create view
    """
    queryset = ClusterTemplateVersionModel.objects.all()
    serializer_class = ClusterTemplateVersionModeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ClusterTemplateVersionFilterSet
    lookup_field = 'template'
    lookup_url_kwarg = 'cluster_template_id'

    def get_queryset(self):
        return super(ClusterTemplateVersionListCreateAPIView, self).get_queryset().filter(
            template=self.kwargs['cluster_template_id'])

    def get_object(self):
        """
        若inherit_version参数指定了版本号,且版本号存在,则继承自改版本,设置object.pk = None; 若指定的版本号不存在, 则返回404响应
        若inherit_version未指定版本号,则取最大版本号
        若该模板尚未创建过版本, 则新建版本,版本号为"1".
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())

            # Perform the lookup filtering.
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

            assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
            )

            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = queryset.get(**filter_kwargs)

            # May raise a permission denied
            self.check_object_permissions(self.request, obj)
        except ObjectDoesNotExist:
            obj = None
        except MultipleObjectsReturned:
            obj = self.get_queryset().order_by('version').last()

        return obj

    def create(self, request, *args, **kwargs):
        version_obj = self.get_object()

        if not version_obj:
            version_obj = ClusterTemplateVersionModel(
                template=ClusterTemplateModel.objects.get(pk=self.kwargs['cluster_template_id']), version=1,
                status=ClusterTemplateVersionStatusModel.objects.get(name='init'))
            version_obj_config = ()
            version_obj_appid = ()
        else:
            version_obj_config = version_obj.config.all() if version_obj.config else ()
            version_obj_appid = version_obj.app_id.all() if version_obj.app_id else ()
            version_obj.pk = None
            version_obj.id = None
            version_obj.status = ClusterTemplateVersionStatusModel.objects.get(name='init')
            version_obj.changes = ''
            version_obj.version += 1

        version_obj.save()
        if version_obj_config:
            version_obj.config = version_obj_config
        if version_obj_appid:
            version_obj.app_id = version_obj_appid
        headers = self.get_success_headers(data={'url': version_obj.get_absolute_url()})
        serializer = self.get_serializer(instance=version_obj)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ClusterTemplateVersionDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    集群模板版本的详情视图, get、post、put、delete
    """
    queryset = ClusterTemplateVersionModel.objects.all()
    serializer_class = ClusterTemplateVersionModeSerializer
    lookup_field = 'version'
    lookup_url_kwarg = 'version'

    def get_queryset(self):
        return super(ClusterTemplateVersionDetailAPIView, self).get_queryset().filter(
            template=self.kwargs['cluster_template_id'])


class ClusterTemplateCreateTemplateView(MatchByUrlTemplateView):

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = '集群模板'
        self.body_header_navigation['page'] = '创建集群模板'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'cluster_template_form': ClusterTemplateForm}
        kwargs.update(context)

        return super(ClusterTemplateCreateTemplateView, self).get_context_data(**kwargs)


class ClusterTemplateDetailTemplateView(MatchByUrlTemplateView):

    template_name = 'arch/clusters/templates/detail.html'

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = '集群模板'
        self.body_header_navigation['page'] = '详情'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'cluster_template_form': ClusterTemplateForm,
                   'cluster_template_id': self.kwargs['pk'],
                   'cluster_template_stable_version_table': 'ClusterTemplateStableVersionTable',
                   'cluster_template_all_version_table': 'ClusterTemplateAllVersionTable'}
        kwargs.update(context)

        return super(ClusterTemplateDetailTemplateView, self).get_context_data(**kwargs)


class ClusterTemplateListTemplateView(MatchByUrlTemplateView):

    template_name = 'arch/clusters/templates/list.html'
    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = '集群模板'
        self.body_header_navigation['page'] = '集群模板列表'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'cluster_template_table': 'ClusterTemplateTable'}
        kwargs.update(context)

        return super(ClusterTemplateListTemplateView, self).get_context_data(**kwargs)


class ClusterTemplateVersionDetailTemplateView(MatchByUrlTemplateView):

    template_name = 'arch/clusters/templates/versions/detail.html'

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['main'] = '集群模板'
        self.body_header_navigation['minor'] = '模板版本详情'
        self.body_header_navigation['page'] = '模板版本号'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'cluster_template_version_form': ClusterTemplateVersionForm, 'version': self.kwargs.get('version')}
        kwargs.update(context)

        return super(ClusterTemplateVersionDetailTemplateView, self).get_context_data(**kwargs)


class ClusterTemplateVersionCreateTemplateView(MatchByUrlTemplateView):

    template_name = 'arch/clusters/templates/versions/create.html'

    body_header_navigation = body_header_navigation

    def get_body_header_navigation(self):
        self.body_header_navigation['minor'] = '集群模板'
        self.body_header_navigation['page'] = '新增版本'
        return self.body_header_navigation

    def get_context_data(self, **kwargs):
        context = {'cluster_template_form': ClusterTemplateVersionForm}
        kwargs.update(context)

        return super(ClusterTemplateVersionCreateTemplateView, self).get_context_data(**kwargs)

