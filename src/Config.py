#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:26
# Email='wangxk1991@gamil.com'
# Desc: 配置处理模块
import config.settings as settings
import logging
import os


class Config():
    builtin = ['system']

    @classmethod
    def init(self):
        global config
        config = {}
        Config.load()

    # 配置文件加载
    # path : config module path
    # name : key of dict
    @classmethod
    def load(self):
        # 加载系统配置
        config['system'] = settings.system
        # 加载自定义的配置文件
        for conf in settings.config:
            if conf['key'] in self.builtin:
                logging.error('配置文件关键字使用了系统内置变量--%s', conf['key'])
                exit()
            if conf['enable'] is True:
                module = __import__(conf['module'])
                if hasattr(module, conf['key']):
                    config[conf['key']] = getattr(getattr(module, conf['key']), conf['key'],
                                                  '配置索引不存在！出错索引:' + conf['key'])

    # 配置项查询
    # key : 配置项
    @classmethod
    def get(self, key=None):
        temp = config
        if key == None:
            return temp
        if '.' in key:
            keys = str.split(key, '.')
            for k in keys:
                if k in temp.keys():
                    temp = temp[k]
                else:
                    logging.error('配置查询出错，出错的索引是：%s', key)
                    exit()
        else:
            temp = temp[key]
        return temp

    # 插入配置项
    # key : 配置项
    @classmethod
    def set(self, key, value):
        if key in self.builtin:
            logging.error('配置文件关键字使用了系统内置变量--%s', key)
        else:
            config[key] = value
