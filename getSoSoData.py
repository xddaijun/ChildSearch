# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 18:49:16 2011
格式化soso的搜索页面，提取其中的链接和文字

@author: mark
"""
import sys
import time
import urllib2
from BeautifulSoup import *



def getfromSOSO(query):
    html = None
    try:
        encodedQuery = query.decode("utf-8").encode("gbk") #utf-8 -> unicode -> self.charset
        fullUrl = r'http://www.soso.com/q?w=%s' + urllib2.quote(encodedQuery)
        res = urllib2.urlopen(fullUrl,None,60) # timeout=60s
        html = res.read()
    except urllib2.URLError, e:
        print "[Error]", e, fullUrl
        sys.exit(-1)
    s=BeautifulSoup(unicode(html,"gbk"))
    outstr=[]
    for liurl in s.findAll('li',attrs={'loc':re.compile("\d")}):
        outstr.append((liurl('a')[0]['href'],liurl('a')[0].getText(),liurl('p')[0].getText))
        #outstr[1]=
    return outstr[0:8]
    #sss=sss[0].find('a',href=re.compile('tv\.sohu\.com'))
    ##sss=soup('a',href=re.compile('tv\.sohu\.com'))[9]['href']
    #return sss # self.charset -> unicode
    
def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    outstr=getfromSOSO("裸婚时代 site:tv.sohu.com")
    print outstr[0]
     


if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)