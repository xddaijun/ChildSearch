# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:49:16 2011

@author: mark
"""
import time
import datetime
import saveSpecialData
import saveSwfData
import MySQLdb
import sys
conn =MySQLdb.Connection(host='localhost', user='root', passwd='mysql', db='childsearch',use_unicode=1, charset='utf8')
def savefun(savedata,tp):
    #print "Hello"
    #curl=Crawl_URL({'url':savedata[2],'name':savedata[0],'gpic':savedata[1],'stype':tp})
    #curl.save()   
    cur =conn.cursor()
    if len(savedata[0])>1:
        cur.execute("insert into  crawl_crawl_url(sdate,url,name,gpic,stype) \
        values('%s','%s','%s','%s','%d')"%(str(datetime.datetime.now()),\
               savedata[2],savedata[0],savedata[1],tp))
        print savedata[0]


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    saveSwfData.startCal(savefun)
    saveSpecialData.startCal(savefun)
    
     
    
if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)
