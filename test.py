#!/usr/bin/env python
from multiprocessing import Process
import os,commands

def task(taskid,time):
    pid = commands.getoutput('echo $$')
    print "pid: ",pid
    print 'time is:',time
    os.system('sleep %d' % int(taskid*2))
for i in range(1,10):
    p = Process(target = task, args = (i,222))
    p.start()

print 'ok'
print 'ok'
