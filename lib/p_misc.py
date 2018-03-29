# -*- coding: utf-8 -*-

import sys,json,time,hashlib,socket,smtplib
from pecan.hooks import PecanHook
from pecan import abort
from email.mime.text import MIMEText
from email.header import Header

class Misc(object):
    def keycheck(self,data,keys):
        if not isinstance(keys,str):
            ret = {"ret":-1,"output":"option key must be a string,sperated by , if multi"}
            return ret
        for key in keys.split(','):
            if key not in data or data[key] == None:
                ret = {"ret":-1,"output":"Key %s is missing or value of key %s is invalid" % (key,key)}
                return ret
    def md5(self,src):
        m2 = hashlib.md5()
        m2.update(src)
        return m2.hexdigest().lower()
    def gettime(self,type):
        if type == 'date':
            ptime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        elif type == 'timestamp':
            ptime = int(time.time())
        return ptime
    def getIPByHost(self,host):
        try:
            result = socket.getaddrinfo(host,None)
            ip = result[0][4][0]
            ret = {"ret":0,"output":ip}
        except Exception as e:
            ret = {"ret":-1,"output":str(e)}
        return ret
    def sendMail(self,subject,content,sender,tolist,cclist=None):
        #to and cc list need be sperated by ';'
        content = '''
    Dear User,please contact bentley.
                                            bentely
                                                    bentley
'''
        smtphost = 'tus3hub-inb-relay.community.veritas.com'
        msg = MIMEText(content,'plain','gb2312')
        msg['Subject'] = Header(subject,'utf-8')
        msg['From'] = Header(sender,'utf-8')
        msg['To'] = Header(tolist,'utf-8')
        receiver = tolist.split(';')
        if cclist:
            msg['Cc'] = Header(cclist,'utf-8')
            receiver.extend(cclist.split(';'))
        try:
            s = smtplib.SMTP()
            s.connect(smtphost)
            s.sendmail(sender,receiver,msg.as_string())
            return {"ret":0,"output":"Successful to send mail."}
        except Exception as e:
            return {"ret":-1,"output":str(e)}
        finally:
            s.quit()
class pacthook(PecanHook):
    def before(self,state):
        ret = None
        #import pdb;pdb.set_trace()
        data = state.arguments.keywords
        if 'appid' not in data:
            ret = "Please input appid for pact do indentity check."
        else:
            appid = data['appid']
            if appid != '123':
                ret = "Unauthorized appid"
        if ret:
            abort(403,ret,None,None)
       
       
class Corshook(PecanHook):
    def before(self,state):
        ret = None
        #import pdb;pdb.set_trace()
        data = state.arguments
        print data
        data = str(data)
        fp = open('/tmp/data','w')
        try:
            content = fp.write(data)
        finally:
            fp.close()
    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
        state.response.headers['Access-Control-Allow-Headers'] = 'Origin,authorization,accept,Content-Type,Access-Control-Allow-Origin'
        if not state.response.headers['Content-Length']:
            state.response.headers['Content-Length'] = str(len(state.response.body))
