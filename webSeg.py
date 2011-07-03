# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 21:08:31 2011
在线分词

@author: mark
"""
from urllib import urlopen,urlencode
import simplejson as json
import time


def postseg(text):
    params = urlencode({'data': text, 'respond': 'json'})
    posturl='http://113.105.93.45/api.php'
    sout=json.load(urlopen(posturl,params))
    return sout['words']

def ismvorgame(words):
    words=words.encode("utf-8")
    words=postseg(words)
    for w in words:        
        if w['attr']=="yx" :
            return ('game',str(int(w['idf']*5000+0.01)))
        elif w['attr'].find('mv')>=0 :
            return ('movie','')
    return ('other','')
    
def main():
    words="我要玩五子连珠"    
    print ismvorgame(words)
    
if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)