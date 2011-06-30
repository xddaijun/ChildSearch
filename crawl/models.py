# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 21:09:06 2011

@author: mark
"""

from django.db import models

class Crawl_URL(models.Model):  
    url = models.URLField(u'抓取地址',max_length=100, unique=True)  
    sdate = models.DateTimeField(u'保存时间',auto_now_add=True,blank=True,null=True)  
    gpic=models.URLField(u'图片地址',max_length=128,null=True)
    name=models.CharField(u'名称',max_length=128,null=True)
    stype=models.CharField(max_length=20,verbose_name=u'用户类型')
    def __unicode__(self):  
        return "%s"%self.name
# Create your models here.
