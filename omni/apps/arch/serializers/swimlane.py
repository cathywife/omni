# -*- coding:utf8 -*-
"""
Created on 16/9/26 上午11:46
@author: fmc

"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function

from rest_framework import serializers
from ..models.swimlane import SwimlaneModel


class SwimlaneModelSerializer(serializers.ModelSerializer):

    class Meta:
        mode = SwimlaneModel
        depth = 1

