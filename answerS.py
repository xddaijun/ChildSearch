# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 21:09:06 2011

@author: mark
"""
import urllib2
from BeautifulSoup import *
import time


def searchByWord(key):
    c=urllib2.urlopen("http://www.baizhitong.com/answer.aspx?qry="+key)
    soup=BeautifulSoup(c.read())
    content=""
    for lli in soup('li')[1:]:
        content=content+"%s"%lli
#    content.
    #content=soup('a',href=re.compile('ansdetail\.aspx\?uid='))[9]['href']
    return content

def main():
    #for w in parsePY("woshiyigerxi'anshi"):
    #    print w
    searchByWord("西安")

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)
    