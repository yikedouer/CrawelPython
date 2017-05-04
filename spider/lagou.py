# coding:utf-8

__author__ = 'HarriesLancer&&'

'''
  该文件实现的是爬取拉勾网的爬虫所必须的一些信息
'''

import logging
import logging.config
import re
import time
import pymongo
from pymongo import MongoClient
from datetime import datetime

#专注于拉勾网的下一页数据爬取
def naxtpageprocessLagou(text):
    pattern=re.compile(r'<a.*?href="(.*?)".*?>下一页</a>')
    match=pattern.search(text)
    if match:
        return match.group(1)
    return ""


#专注于拉勾网的url抽取工作
def extractUrlLagou(text):
    urls=[]
    pattern=re.compile(r'(https://www.lagou.com/jobs/\d+?.html)')
    match=pattern.findall(text)
    for i in match:
        urls.append(i.strip())
    return urls

#保存数据
def savePageLagou(datamap):
    client=MongoClient("mongodb://219.216.65.201:27017")
    db=client.RawPageDB
    for key in datamap.keys():
        page=datamap[key]
        db.lagou.insert_one({
            "url":key,
            "context":page,
            "time":time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        })
    datamap.clear()
    #db.close()
    client.close()