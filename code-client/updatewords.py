# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 17:27:14 2011

@author: mark
"""

import time
import re
import sys

dicts=open('/home/mark/cpp/phptool_for_scws_xdb/dict.txt')
wordsset=set()
alllines = dicts.readlines( )
for line in alllines:
    line=line.strip()
    if line[0]!='#':
         words=line.split()
         wordsset.add(words[0])
dicts.close()

def parseFromSql():
    f=open('out.txt','r')
    g=open('game.txt','w')    
    alllines = f.readlines( )
    for line in alllines:
        word=line.split()
        if int(word[-1][2:])>5000:     
            try:
                w=re.sub(r"下载","",word[0])
                w=re.sub(r"小游戏","",word[0])
                w=re.sub(r"[A-Za-z0-9]{2,}","",w)
                w=re.sub(r"(\-\w*$)","",w)
                w=w.strip()
                if len(w)<=6:
                    continue
                if w in wordsset and len(w)<=9:
                    print w
                    continue
                if w.find("-")>=0 or w.find("_")>=0 or w.find("专题")>=0:
                    continue
                highnum=(int(word[-1][2:]))/5000.0
                #lownum=(int(word[-1][2:])%100)/10.0
                print>>g,("%s\t10.41\t%.4f\tyx")%(w,highnum)
            except Exception, what:
                print what       
    f.close()
    g.close()

def parseFromSougou():
    files=['电视剧集合.txt','中外电影名称.txt','综艺节目名.txt','最全影视词库.txt']
    g=open('movie.txt','w')
    for f in files:
        fs=open(f,'r')
        alllines = fs.readlines( )
        for line in alllines:
            word=line.strip()            
            print>>g,("%s\t10.42\t10.32\tmv")%word
    g.close()
            
     

def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    parseFromSougou()
    parseFromSql()
     
    
if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)