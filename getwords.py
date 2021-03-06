# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 16:37:12 2011
读取QQ输入法的拼音结果，将拼音转化为汉字

@author: mark
"""

from urllib import urlopen
import simplejson as json
import time
import re


def getQQWords(preword,pys,curNum): 
    global wordsSet    
    if(len(pys)<1 and preword not in wordsSet):     
       wordsSet.append(preword)
       return
    if curNum>1:
        nextNum=curNum-1
    else:
        nextNum=1
    pylen=len(pys)
    sout=json.load(urlopen("http://ime.qq.com/fcgi-bin/getword?q=%s" % pys))
    ix=0
    while(pylen>=1 and ix<curNum):
        getQQWords(preword+sout['rs'][ix],pys[int(sout['rsn'][ix]):],nextNum)
        ix=ix+1

def parsePY(inputStr):
    global wordsSet    
    outwords=[]
    match = re.search(r'^[a-zA-Z\'\s]+$', inputStr)
    if match:        
        matches=re.split("\s",inputStr)
        ix=0
        if len(matches)>1:             
            outwords.append("")
            while ix<len(matches):
                wordsSet=[]
                getQQWords("",matches[ix],1)
                outwords[0]=outwords[0]+wordsSet[0]+" "
                ix=ix+1
        else:
            wordsSet=[]
            getQQWords("",matches[ix],3)
            outwords=wordsSet
    return outwords        

def main():
    for w in parsePY("woshiyigerxi'anshi"):
        print w

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)