# coding:utf-8

__author__ = 'HarriesLancer&&'

import threading
import requests   #替换urllib的第三方类库
import time
import random
import logging
import logging.config



from doc.head import  headerdata

'''
实现的通用爬虫类---按照翻页形式爬取的,继承多线程类
'''
class crawelbypage(threading.Thread):

    urlToSave={} #需要保存的url
    urlHave=[] #已经爬取的url
    urlnew=[]#本次爬取过程新爬取的url
    nextpageurl="" #下一步爬取的url
    headesMap={}

    def __init__(self,name,nextpageprocess,extracturl,logger,savemethod): #构造函数，name--爬虫的名称,nextpageprocess--获取下一页的方法,extracturl--获取url的方法
        threading.Thread.__init__(self)
        self.name=name
        self.nextPageProcess=nextpageprocess
        self.extracturl=extracturl
        self.logger=logger #传入的日志文件
        self.savemethod=savemethod

    def SaveMethod(self): #获取当前的存储方法
        self.savemethod(self.urlToSave)
        self.logger.info("%s crawel:save data already!",self.name)

    def run(self):#真正的爬虫运行方法-----重写threading.Thread类
        while True:
          for i in range(self.pagenumber): #读取pagenumber页
              self.headesMap['User-Agent']=headerdata[random.randint(0,len(headerdata)-1)]
              r=requests.get(url=self.nextpageurl,headers=self.headesMap)
              self.logger.info("%s crawel:the page url is getting %s",self.name,self.nextpageurl)
              self.nextpageurl=self.nextPageProcess(r.text)
              self.urlnew.extend(self.extracturl(r.text))
              self.logger.info("%s crawel:get %d jobs url",self.name,len(self.urlnew))
              for url1 in self.urlnew: #抽取每一页的合法连接进行获取
                 if url1 not in self.urlHave:
                     url_data=requests.get(url=url1,headers=self.headesMap)
                     self.logger.info("%s crawel:now get %s",self.name,url1)
                     self.urlToSave[url1]=url_data.text
              self.writeFile()

          self.SaveMethod() #将本次读取的数据存储下来

          self.logger.info("%s crawel:thread is slepping, may awake on tomorrow",self.name)
          time.sleep(60*60*random.randint(20,30)) #整个线程休息20-30个小时，再执行下一次爬取





    def writeFile(self):#将新爬取的数据加入到数据中
        file_object=open(self.name,'a+')
        for i in self.urlnew:
            file_object.write(i+"\n")
        file_object.close()
        self.logger.info("%s crawel:append %d urls in lagou.txt",self.name,len(self.urlnew))
        self.urlHave.extend(set(self.urlnew))
        self.urlnew.clear()


    def begining(self,beginurl,number):#爬虫初始化方法--beginurl初始爬取的url,number一次最多爬取的页数
        self.nextpageurl=beginurl
        self.pagenumber=number
        self.logger.info("%s crawel:begin page url %s,number %d",self.name,beginurl,number)
        #从文件中读取相关数据
        file_object=open(self.name,'r')
        data=file_object.readlines()
        for data_item in data:
            self.urlHave.append(data_item.strip())
        self.logger.info("%s crawel:read %d old urls",self.name,len(data))
        file_object.close()




