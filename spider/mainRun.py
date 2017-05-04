# coding:utf-8

__author__ = 'HarriesLancer&&'



import logging
import logging.config


from common.crawel import crawelbypage
from spider.lagou import naxtpageprocessLagou
from spider.lagou import extractUrlLagou
from spider.lagou import savePageLagou

logging.config.fileConfig("logger.conf")
logger=logging.getLogger("infoLogger")

lagoucrawel=crawelbypage("lagou",naxtpageprocessLagou,extractUrlLagou,logger,savePageLagou)  #创建拉钩爬虫
lagoucrawel.begining("https://www.lagou.com/zhaopin/",1)
lagoucrawel.start()