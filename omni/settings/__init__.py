# -*- coding:utf8 -*-
"""
Created on 2015年1月4日
    初始化settings
@author: FMC
"""
from __future__ import print_function, unicode_literals, division, absolute_import

# 导入通用设置
from .common import *


# 导入环境特定配置
try:
    from omni.settings.dev import *
    from omni.settings.test import *
    from omni.settings.pre import *
    from omni.settings.prod import *
except ImportError:
    pass
