# -*- coding:utf8 -*-
"""
Created on 16/10/5 上午2:28
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from omni.libs.django.model.common import CreateUpdateDateTimeCommonModelMixin


class UserModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='用户名,英文字符/数字')
    visible_name = models.CharField(blank=True, max_length=50, help_text='用户显示名')
    description = models.CharField(blank=True, max_length=100, help_text='描述、说明信息')
    usergroup = models.ManyToManyField('UserGroupModel', db_table='user_relate_usergroup',
                                       blank=True, null=True, help_text='所属用户组列表')
    email = models.EmailField(blank=True, help_text='邮件地址')
    department = models.ForeignKey('UserDepartmentModel', help_text='用户所属部门', null=True, blank=True)

    class Meta:
        db_table = 'user'


class UserGroupModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='用户组,英文字符/数字')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='用户组显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')

    class Meta:
        db_table = 'user_group'


class UserDepartmentModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    name = models.CharField(max_length=50, unique=True, help_text='部门名称')
    visible_name = models.CharField(blank=True, null=True, max_length=50, help_text='部门显示名')
    description = models.CharField(blank=True, null=True, max_length=100, help_text='描述、说明信息')

    class Meta:
        db_table = 'user_department'

    def get_absolute_url(self):
        return reverse('template-cmc:department-detail', args=[str(self.id)])


class PermissionProductUserGroupModel(CreateUpdateDateTimeCommonModelMixin, models.Model):
    usergroup = models.ForeignKey(UserGroupModel, on_delete=models.SET_NULL, db_constraint=False, verbose_name='用户组',
                                  help_text='关联的用户组')
    product = models.ForeignKey('arch.ProductModel', on_delete=models.SET_NULL, db_constraint=False, verbose_name='产品',
                                help_text='关联的产品')
    project = models.ForeignKey('arch.ProjectModel', on_delete=models.SET_NULL, db_constraint=False, verbose_name='项目',
                                help_text='关联的项目', null=True)
    appid = models.ForeignKey('arch.AppIdModel', on_delete=models.SET_NULL, db_constraint=False, verbose_name='AppID',
                              help_text='关联的AppID', null=True)
    is_owner = models.BooleanField(verbose_name='是否Owner', help_text='是否Owner', default=False)
    # permission = models.ManyToManyField()

    class Meta:
        db_table = 'user_group_permission_product'

