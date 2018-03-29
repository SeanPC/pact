import json
import commands
from p_misc import Misc
from p_os import Cmd
from p_mysql import Database
misc = Misc()
cmd = Cmd()
db = Database()

#client will be public to all when poolid=0 and will be private to users when poolid=10000
#status:0:Not Avaiable
#status:1:Avaiable
#status:2:In Use

class Client(object):
    def getNode(self,user_id):
        sql = "select pool from user where id=%s;" % user_id
        pool = db.mysql(sql)
        if pool['ret'] == -1:
            poolid = 10001
        else:
            poolid = pool['output'][0][0]
        sql = "select id,hostname from client where status=1 and (pool in (0,%s) or user_id=%s);" % (poolid,user_id)
        return db.get({"sql":sql})
    def setAuth(self,host,user,password):
        sql = "select name from driver;"
        driver = db.mysql(sql)
        if driver['ret'] == -1:
            driver['output'] = "Failed to get driver names as reason [%s]" % driver['output']
            return driver
        else:
            driver = [i[0] for i in driver['output']]
            driver = ','.join(driver)
            source = 'pact,' + driver
        result = cmd.setupAuth(host,user,password,source)
        if result['ret'] == -1:
            result['output'] = "Failed to setup equivalence to client as reason [%s]" % result['output']
        else:
            result['output'] = "Successful to setup equivalence to the client."
        return result       
    def post(self,data):
        ret = misc.keycheck(data,'name,user,password,pool,site,clus_flag,user_id')
        if ret:
            return json.dumps(ret)
        ip = misc.getIPByHost(data['name'])
        if ip['ret'] == -1:
            return json.dumps(ip)
        else:
            ip = ip['output']
        result = self.setAuth(data['name'],data['user'],data['password'])
        if result['ret'] == 0:
            sql = "insert into client (hostname,user,ip,password,status,pool,site,task_id,clus_flag,user_id) values ('%s','%s','%s','%s',1,%s,%s,0,%s,%s);" % (data['name'],data['user'],ip,data['password'],data['pool'],data['site'],data['clus_flag'],data['user_id'])
            result = db.mysql(sql)
            if result['ret'] == -1:
                result['output'] = "Failed to add a client as reason [%s]" % result['output']
            else:
                result['output'] = "Successful to add the client with the client id [%s]" % result['output']
        else:
            result['output'] = "Failed to add a client as reason [%s]" % result['output']
        return json.dumps(result)
    def delete(self,data):
        ret = misc.keycheck(data,'id,name')
        if ret:
            return json.dumps(ret)
        sql = "select status from client where id=%s;" % data['id']
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to get client status as reason [%s]" % result['output']
        elif result['output'][0][0] == 2:
            result['output'] = "Client %s is in use" % data['name']
        else:
            sql = "delete from client where id=%s;" % data['id']
            result = db.mysql(sql)
            if result['ret'] == -1:
                result['output'] = "Failed to delete a client as reason [%s]" % result['output']
            else:
                result['output'] = "Successful to delete the client %s" % data['name']   
        return json.dumps(result)
    def updateProfile(self,name,user,password,status,site,clus_flag,id):
        sql = "update client set hostname='%s',user='%s',password='%s',status='%s',site=%s,clus_flag=%s where id=%s ;" % (name,user,password,status,site,clus_flag,id)
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to update client %s as reason [%s]." % (name,result['output'])
        else:
            result['output'] = "Successful to update the client %s" % name
        return result
    def updateOwnership(self,pool,user_id,id):
        sql = "update client set pool=%s,user_id=%s where id=%s;" % (pool,user_id,id)
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to update onwership for client %s as reason [%s]." % (name,result['output'])
        else:
            result['output'] = "Successful to update onwership for the client %s" % name
        return result        
    def updateTaskid(self,task_id,id):
        sql = "update client set task_id='%s' where id=%s ;" % (task_id,id)
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to update task_id for client %s as reason [%s]." % (name,result['output'])
        else:
            result['output'] = "Successful to update task_id for the client %s" % name
        return result
    def checkAndUpdateStatus(self,name,id):
        sql = "select status from client where id=%s;" % id
        status = db.mysql(sql)
        if status['ret'] == -1:
            return {"ret":-1,"output":"Failed to get current status as reason [%s]" % status['output']}
        else:
            status = status['output'][0][0]
        result = cmd.rexec(name,'root','nop','hostname',60)
        if result['ret'] == 0 and status == 0:
            sql = "update client set status=1 where id=%s" % id
        elif result['ret'] == -1 and status == 1:
            sql = "update client set status=0 where id=%s" % id
        if sql:
            result = db.mysql(sql)
            if result['ret'] == 0:
                result['output'] = "Successful to update status for the client %s" % name
            else:
                result['output'] = "Failed to update status for client %s as reason [%s]." % (name,result['output'])
        else:
            result = {"ret":0,"output":"No Need to update status for client"}
        return result
    def put(self,data):
        ret = misc.keycheck(data,'type,name,id')
        if ret:
            return json.dumps(ret)
        type = data['type']
        id = data['id']
        name = data['name']
        if type == 'profile':
            ret = misc.keycheck(data,'name,user,password,status,site,clus_flag')
            if ret:
                return json.dumps(ret)
            result = self.updateProfile(data['name'],data['user'],data['password'],data['status'],data['site'],data['clus_flag'],id)
        elif type == 'ownership':
            ret = misc.keycheck(data,'pool,user_id')
            if ret:
                return json.dumps(ret)
            result = self.updateOwnership(data['pool'],data['user_id'],name,id)
        elif type == 'taskid':
            ret = misc.keycheck(data,'task_id')
            if ret:
                return json.dumps(ret)       
            result = self.updateTaskid(data['task_id'],name,id)
        elif type == 'status':    
            result = self.checkAndUpdateStatus(name,id)
        elif type == 'setAuth':
            sql = "select password from client where id=%s" % id
            result = db.mysql(sql)
            if result['ret'] == -1:
                result['output'] = "Failed to get user,password as reason [%s]." % result['output']
                return result
            else:
                user = result['output'][0][0]
                password = result['output'][0][1]
            result = self.setAuth(name,user,password)
        else:
            result = {"ret":-1,"output":"Invalid type in client.put"}
        return json.dumps(result)
    def getList(self):
        sql = "select name,status,site,clus_flag,pool,user_id from client;"
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to get list as reason [%s]." % result['output']
            return result
        else:
            output = []
            list = result['output']
            for result in list:
                if result[4] == 0:
                    owner = public
                elif result[4] == 10000:
                    sql = "select username from user where id=%s;" % result[5]
                    user = db.mysql(sql)
                    if user['ret'] == -1:
                        user['output'] = "Failed to get user name as reason [%s]" % user['output']
                        return user
                    owner = user['output'][0][0]
                else:
                    sql = "select name from pool where id=%s;" % result[4]
                    pool = db.mysql(sql)
                    if pool['ret'] == -1:
                        pool['output'] = "Failed to get pool name as reason [%s]" % pool['output']
                        return pool
                    owner = pool['output'][0][0] 
                output0 = {"name":result[0],"status":result[1],"site":result[2],"clus_flag":result[3],"owner":owner}
                output.append(output0)
            result = {"ret":0,"output":output}
            return result
    def get(self,data):
        ret = misc.keycheck(data,'type')
        if ret:
            return json.dumps(ret)
        if type == 'list':
            result = self.getList()
        elif type == 'attri':
            ret = misc.keycheck(data,'id')
            if ret:
                return json.dumps(ret)
            sql = "select * from client where id=%s" % data['id']
            return db.get(sql)
        elif type == 'nodeForUser':
            ret = misc.keycheck(data,'user_id')
            if ret:
                return json.dumps(ret)        
            return self.getNode(data['user_id'])
        else:
            result = {"ret":-1,"output":"Invalid type in client.get"}
        return json.dumps(result)            