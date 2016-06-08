# -*- coding:utf8 -*-
"""
Created on 2015年1月5日
    软件相关数据表
@author: FMC
"""

from .base import BaseSoftwareModel
from django.db import models


class GitModel(BaseSoftwareModel):
    """
    Git软件
    """
    class Meta:
        db_table = 'software_git'


class JdkModel(BaseSoftwareModel):
    """
    Jdk软件
    """
    class Meta:
        db_table = 'software_jdk'


class JenkinsCliModel(BaseSoftwareModel):
    """
    JenkinsCli软件
    """
    class Meta:
        db_table = 'software_jenkins_cli'


class MavenModel(BaseSoftwareModel):
    """
    Maven软件
    """
    settings_path = models.FilePathField(blank=True, null=True, max_length=300, help_text='settings.xml文件所在路径')
    settings_content = models.TextField(blank=True, null=True, help_text='settings.xml配置文件内容')
    default_lifecycle = models.CharField(blank=True, null=True, max_length=300, help_text='默认生命周期')
    default_opts = models.CharField(blank=True, null=True, max_length=50, help_text='默认选项')

    class Meta:
        db_table = 'software_maven'


class PythonModel(BaseSoftwareModel):
    """
    Python软件
    """
    class Meta:
        db_table = 'software_python'
    

class RsyncModel(BaseSoftwareModel):
    """
    Rsync软件
    """
    class Meta:
        db_table = 'software_rsync'
    
    
class SubversionModel(BaseSoftwareModel):
    """
    Subversion软件
    """
    class Meta:
        db_table = 'software_subversion'
