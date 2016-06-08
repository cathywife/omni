# !/usr/bin/env python
# -*- coding:utf8 -*-
"""
Created on 2015年2月9日
    服务Mixin模块
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

import logging

log = logging.getLogger(__name__)

from omni.apps import ByIdentityResourceBaseMixin
from omni.apps.service.models import SvnAuthModel, SvnRepositoryModel, SvnServerModel, GitAuthModel, \
    GitRepositoryModel, GitServerModel


class SvnAuthModelMixin(ByIdentityResourceBaseMixin):
    model = SvnAuthModel


class SvnServerModelMixin(ByIdentityResourceBaseMixin):
    model = SvnServerModel


class SvnRepositoryModelMixin(ByIdentityResourceBaseMixin):
    model = SvnRepositoryModel


class GitServerModelMixin(ByIdentityResourceBaseMixin):
    model = GitServerModel


class GitRepositoryModelMixin(ByIdentityResourceBaseMixin):
    model = GitRepositoryModel


class GitAuthModelMixin(ByIdentityResourceBaseMixin):
    model = GitAuthModel