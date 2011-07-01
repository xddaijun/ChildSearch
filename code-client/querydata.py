# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:27:14 2011

@author: mark
"""

import time
import datetime
import saveSpecialData
import saveSwfData
import MySQLdb
import sys
conn =MySQLdb.Connection(host='localhost', user='root', passwd='mysql', db='childsearch',use_unicode=1, charset='utf8')

def main():
    f=open('out.txt','w')
    reload(sys)
    sys.setdefaultencoding('utf-8')
    cur =conn.cursor()
    cur.execute("select * from crawl_crawl_url")    
    rows=cur.fetchall()
    for r in rows:
        print>>f,("%s\t10.42\t10.32\tyx")%r[4]
    f.close()
    
     
    
if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)