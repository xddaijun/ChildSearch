# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 21:09:06 2011

@author: mark
"""
import urllib2
from BeautifulSoup import *
import time
import re


def searchByWord(key):
    key=key.encode("utf-8")
    c=urllib2.urlopen("http://www.baizhitong.com/answer.aspx?qry="+key)
    soup=BeautifulSoup(c.read())
    content=""
    for lli in soup('li')[1:]:
        content=content+"%s"%lli
    content=re.sub("ansdetail.aspx","/showpage",content)
    #content=soup('a',href=re.compile('ansdetail\.aspx\?uid='))[9]['href']
    return content
def getContent(uid):
    c=urllib2.urlopen("http://www.baizhitong.com/ansdetail.aspx?uid="+uid)
    soup=BeautifulSoup(c.read())
    content = soup.find('div',attrs={'id':'best_answer_content'}).find('pre')
    return content

    

def main():
    #print searchByWord("西安")
    print getContent("aHR0cDovL3poaWRhby5iYWlkdS5jb20vcXVlc3Rpb24vMjc2MjU5NDI5Lmh0bWw/YW49MCZzaT0xNw==")

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)
    