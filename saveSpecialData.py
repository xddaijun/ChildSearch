# -*- coding: utf-8 -*-
'''
Created on Thu Jun 30 11:50:16 2011

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
                gamename,gamepic,gamepath = self.parse(req)
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
    f = Crawler(threads=30,parsefun=getswfgame)
    for i in range(14400,14500,3):
        f.push_req("http://www.7k7k.com/swf/%.5d.htm"%i) 
   
    while f.taskleft():        
        savefun(f.pop())
        
def getfromgoogle(url):
    s=json.load(urllib2.urlopen(url))['responseData']['results']   
    return [s[0]['url'],s[1]['url'],s[2]['url'],s[3]['url']]

 
def getspecialgame(url):
    c=urllib2.urlopen(url)
    s=BeautifulSoup(c.read())
    gamename=s.html.head.title.string.split(',')[0]
    gameurl=str(s.find('iframe'))
    return (gamename,'-1',gameurl)
    
    
def main():
    pass
    #startCal()
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