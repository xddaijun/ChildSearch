# -*- coding: utf-8 -*-
'''
Created on Thu Jun 30 11:50:16 2011
读取谷歌http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=的搜索结果，
提取其中的URL部分，提取完URL，再对URL进行结构化抽取。并存入数据库
@author: mark
'''
import urllib2
from BeautifulSoup import *
from Queue import Queue
from threading import Thread,Lock,stack_size
import time
import simplejson as json
import threading
stack_size(32768*16)

class Crawler(threading.Thread):
    def __init__(self,threads):
        self.lock = Lock() #线程锁
        self.q_req = Queue() #初始任务队列       
        self.q_target = Queue() #目标任务队列       
        self.q_ans = Queue() #完成队列
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0
        
    def __del__(self): #解构时需等待三个队列完成
        time.sleep(0.5)
        self.q_req.join()
        self.q_target.join()
        self.q_ans.join()
 
    def taskleft(self):
        return self.q_req.qsize()+self.running+self.q_target.qsize()
 
    def push_req(self,req):
        self.q_req.put(req)
 
    def pop(self):
        return self.q_ans.get()
 
    def threadget(self):
        while True:
            if self.q_req.qsize()>=1:
                req = self.q_req.get()
                with self.lock:
                    self.running += 1
                try:
                    urls = getfromgoogle(req)
                except Exception, what:
                    urls=None
                    print what
                if urls:
                    for u in urls:
                        self.q_target.put(u)
                with self.lock:
                    self.running -= 1
                self.q_req.task_done()   
                
            else:                    
                req = self.q_target.get()
                with self.lock:
                    self.running += 1
                try:
                    gamename,gamepic,gamepath = getspecialgame(req)
                except Exception, what:
                    gamename = ''
                    print what
                if len(gamename)>=1:
                    self.q_ans.put((gamename,gamepic,gamepath))
                with self.lock:
                    self.running -= 1
                self.q_target.task_done()              
            time.sleep(0.2) # don't spam
def startCal(savefun):
    f = Crawler(threads=10)
    url='http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=inurl:www.7k7k.com/special/%20site:7k7k.com'
    for i in range(0,32,4):
        f.push_req("%s&start=%d"%(url,i))    
    while f.taskleft():        
        savefun(f.pop(),1)
        
def getfromgoogle(url):
    s=json.load(urllib2.urlopen(url))['responseData']['results']
    return [s[0]['url'],s[1]['url'],s[2]['url'],s[3]['url']]

 
def getspecialgame(url):
    c=urllib2.urlopen(url)
    s=BeautifulSoup(c.read())
    gamename=s.html.head.title.string.split(',')[0]
    gameurl=str(s.find('iframe'))
    return (gamename,'-1',gameurl)
def sf(pp,tp):
    print pp,1    
    
def main():
    startCal(sf)
    #getswfgame('http://www.7k7k.com/swf/58162.htm')
    #getspecialgame('http://www.7k7k.com/special/zhiwu/')
    #for w in parsePY("woshiyigerxi'anshi"):
    #    print w
    #searchByWord("西安")

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)