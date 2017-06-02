# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework import serializers
from ..models.user import UserModel, UserGroupModel, UserDepartmentModel


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        depth = 1


class UserGroupModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserGroupModel
        depth = 1


class UserDepartmentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDepartmentModel
        depth = 1

