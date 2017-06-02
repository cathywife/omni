# -*- coding:utf8 -*-
"""
    FMC 创建于 2014年8月26日
    日志配置文件
"""
import os.path
from . import BASE_DIR
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    #日志格式
    'formatters': {
        'detailed': {
            'format': '%(levelname)-8s %(asctime)s %(name)-20s[line %(lineno)-4d] %(processName)-10s %(threadName)-10s %(remoteip)-12s %(user)-20s %(message)s'
        },
        'localdetailed': {
            'format': '%(levelname)-8s %(asctime)s %(name)-20s[line %(lineno)-4d] %(processName)-10s %(threadName)-10s %(message)s'
        },
        'modulefmdetailed': {
            'format': '%(levelname)-8s %(asctime)s %(name)-20s[line %(lineno)-4d] %(processName)-10s %(threadName)-10s %(message)s'
        },
        'summary': {
            'format': '%(levelname)-8s %(asctime)s %(name)-20s[line %(lineno)-4d] %(message)s'
        },
        'access': {
            'format': '%(asctime)s %(remoteip)-12s %(user)-20s %(path)'
        },
    },
    #过滤器
    'filters': {

    },
    #处理器
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'localdetailed'
        },
        'modulefmconsole':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'modulefmdetailed'
        },
        'logtofile':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs','omms_error.log'),
            'maxBytes': 102400,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'localdetailed'
        },
        'modulefmtofile':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs','omms_error.log'),
            'maxBytes': 102400,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'modulefmdetailed'
        },
        'accesslogtofile':{
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR,'logs','omms_access.log'),
            'maxBytes': 102400,
            'backupCount': 7,
            'encoding': 'utf-8',
            'formatter': 'summary'
        },
        # 'mail_admins': {
        #    'level': 'ERROR',
        #    'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['special']
        # }
    },
    #记录器
    'loggers': {
        '': {
            'handlers': ['console', 'logtofile'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django': {
            'handlers': ['console', 'logtofile'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['modulefmconsole', 'accesslogtofile'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}