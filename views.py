# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:45:46 2011

@author: mark
"""
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
import getwords
import answerS
import webSeg
import getSoSoData

def checkPY(request):
    if 'q' in request.GET:
        keyword=request.GET["q"]
        outwords=getwords.parsePY(keyword)
        if len(outwords)>0:            
            return render_to_response('index.html',locals())
        #keyword=keyword.encode("utf-8")
        if keyword.find(u"哪")>=0 or keyword.find(u"什么")>=0 or \
        keyword.find(u"怎么")>=0 or keyword.find(u"为什么")>=0 \
        or keyword.find(u"多少")>=0 or keyword.find(u"如何")>=0:
            content=answerS.searchByWord(keyword)                
            return render_to_response('answer.html',locals())
        elif webSeg.ismvorgame(keyword)[0]=='game':
            return render_to_response('game.html',locals())
        elif webSeg.ismvorgame(keyword)[0]=='movie':
            liurls=getSoSoData.getfromSOSO("%s  site:tv.sohu.com"%keyword.encode("utf-8"))
            return render_to_response('movie.html',locals())
        else:
            content=answerS.searchByWord(keyword.encode("utf-8"))                
            return render_to_response('answer.html',locals())
    else:
        return render_to_response('index.html')

def default(request):
    return render_to_response('index.html')


def showpage(request):
    if 'uid' in request.GET:
        uid=request.GET["uid"]
        content=str(answerS.getContent(uid))
        return render_to_response('answerPage.html',locals())
    else:
        return render_to_response('index.html')

