import json
from p_misc import Misc
from p_mysql import Database
misc = Misc()
db = Database()

class Sendmail(object):
    def genContent(self,content_option):
        template = {}
        content_list = content_option.split(',,,')
        return 1
    def post(self,data):
        ret = misc.keycheck(data,'subject,content,sender,tolist') 
        if ret:
            return json.dumps(ret)
        content = self.genContent(data['content'])
        if misc.keycheck(data,'cclist'):
            result = misc.sendMail(data['subject'],data['content'],data['sender'],data['tolist'])
        else:
            result = misc.sendMail(data['subject'],data['content'],data['sender'],data['tolist'],data['cclist'])
        return json.dumps(result)
class Event(object):
    def post(self,data):
        ret = misc.keycheck(data,'level,content')
        if ret:
            return json.dumps(ret)
        date = misc.gettime('timestamp')
        sql = "insert into event values (NULL,%s,'%s','%s');" % (date,date['level'],data['content'])
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to log the event as reason [%s]" % result['output']
        else:
            result['output'] = "Succesful to log the event"
        return json.dumps(result)
    def get(self,data):
        sql = "select id,date,level,content from event;"
        return db.get({"sql":sql})
class Pool(object):
    def checkPoolIsUsed(self,pool_id):
        sql = "select count(id) from user where pool=%s;,,,select count(id) from client where pool=%s;" % (pool_id,pool_id)
        result = db.mysql(sql)
        if -1 in [i['ret'] for i in result]:
            return {"ret":0,"output":"Failed to get if pool is used"}
        for i in result:
            if i['output'][0][0] > 0:
                return {"ret":0,"output":"Pool is in use"}
        return {"ret":-1,"output":"Pool is in not use"}    
    def post(self,data):
        ret = misc.keycheck(data,'name,descrip')
        if ret:
            return json.dumps(ret)
        sql = "insert into pool (name,descrip) values ('%s','%s')" % (data['name'],data['descrip'])
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to add pool %s as reason [%s]" % (data['name'],result['output'])
        else:
            result['output'] = "Succesful to add pool %s." % data['name']
        return json.dumps(result)        
    def delete(self,data):
        ret = misc.keycheck(data,'id,name')
        if ret:
            return json.dumps(ret)    
        pool_id = data['id']
        pooluse = self.checkPoolIsUsed(pool_id)
        if pooluse['ret'] == -1:
            sql = "delete from pool where id=%s;" % id
            result = db.mysql(sql)
            if result['ret'] == -1:
                result['output'] = "Failed to delete pool %s as reason [%s]" % (data['name'],result['output'])
            else:
                result['output'] = "Succesful to delet pool %s." % data['name']
        else:
            result = {"ret":-1,"output":"Pool is in use,can not delete it"}
        return json.dumps(result)
    def put(self,data):
        ret = misc.keycheck(data,'id,name,descrip')
        if ret:
            return json.dumps(ret)            
        sql = "update pool set name='%s',descrip='%s;' where id=%s" % (data['name'],data['descrip'],data['id'])
        if result['ret'] == -1:
            result['output'] = "Failed to update pool %s as reason [%s]" % (data['name'],result['output'])
        else:
            result['output'] = "Succesful to update pool %s." % data['name']
        return json.dumps(result)            
    def get(self,data):
        sql = "select id,name,descrip from pool;"
        return db.get({"sql":sql})
class Site(object):
    def checkSiteIsUsed(self,site_id):
        sql = "select count(id) from user where site=%s;,,,select count(id) from client where pool=%s;" % (site_id,site_id)
        result = db.mysql(sql)
        if -1 in [i['ret'] for i in result]:
            return {"ret":0,"output":"Failed to get if site is used"}
        for i in result:
            if i['output'][0][0] > 0:
                return {"ret":0,"output":"site is in use"}
        return {"ret":-1,"output":"Site is in not use"}    
    def post(self,data):
        ret = misc.keycheck(data,'name,descrip')
        if ret:
            return json.dumps(ret)
        sql = "insert into site (name,descrip) values ('%s','%s')" % (data['name'],data['descrip'])
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to add site %s as reason [%s]" % (data['name'],result['output'])
        else:
            result['output'] = "Succesful to add site %s." % data['name']
        return json.dumps(result)        
    def delete(self,data):
        ret = misc.keycheck(data,'id,name')
        if ret:
            return json.dumps(ret)    
        pool_id = data['id']
        pooluse = self.checkSiteIsUsed(pool_id)
        if pooluse['ret'] == -1:
            sql = "delete from site where id=%s;" % id
            result = db.mysql(sql)
            if result['ret'] == -1:
                result['output'] = "Failed to delete site %s as reason [%s]" % (data['name'],result['output'])
            else:
                result['output'] = "Succesful to delet site %s." % data['name']
        else:
            result = {"ret":-1,"output":"Site is in use,can not delete it"}
        return json.dumps(result)
    def put(self,data):
        ret = misc.keycheck(data,'id,name,descrip')
        if ret:
            return json.dumps(ret)            
        sql = "update site set name='%s',descrip='%s;' where id=%s" % (data['name'],data['descrip'],data['id'])
        if result['ret'] == -1:
            result['output'] = "Failed to update site %s as reason [%s]" % (data['name'],result['output'])
        else:
            result['output'] = "Succesful to update site %s." % data['name']
        return json.dumps(result)            
    def get(self,data):
        sql = "select id,name,descrip from site;"
        return db.get({"sql":sql})