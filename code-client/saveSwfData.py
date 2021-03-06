# -*- coding: utf-8 -*-
'''
Created on Thu Jun 30 11:50:16 2011
多线程读取7k7k.com的单个游戏，结构化抽取其中的swf页面，并保存到数据库中
@author: mark
'''
import urllib2
import sys
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
        self.q_ans.join()
 
    def taskleft(self):
        return self.q_req.qsize()+self.running
 
    def push_req(self,req):
        self.q_req.put(req)
 
    def pop(self):
        return self.q_ans.get()
 
    def threadget(self):
        while True:                
            req = self.q_req.get()
            with self.lock:
                self.running += 1
            try:
                gamename,gamepic,gamepath = getswfgame(req)
            except Exception, what:
                gamename = ''
                print what,req
            if len(gamename)>=1:
                self.q_ans.put((gamename,gamepic,gamepath))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()  
            time.sleep(0.2) # don't spam
          
            
def startCal(savefun):    
    f = Crawler(threads=30)
    for i in range(10000,60000):
        f.push_req("http://www.7k7k.com/swf/%.5d.htm"%i) 
   
    while f.taskleft():
        savefun(f.pop(),2)        
  
def getswfgame(url):
  
    c=urllib2.urlopen(url)
    s=BeautifulSoup(c.read())
    
    match= re.search(r'_gamename = "([^\s"]+)",[\w\W]+, _gamepic = "([^\s"]+)",[\w\W]+, _gamepath = "([^\s"]+)",' ,str(s.head))
    if match:
        return (match.group(1),match.group(2),match.group(3))
    else:
        return ('','','')        

    
def main():
    pass
    #startCal()
    #print getswfgame('http://www.7k7k.com/swf/10462.htm')
    #getspecialgame('http://www.7k7k.com/special/zhiwu/')
    #for w in parsePY("woshiyigerxi'anshi"):
    #    print w
    #searchByWord("西安")

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'use time :%f' % (end-start)