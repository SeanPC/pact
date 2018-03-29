import json,re,os
import commands
from p_misc import Misc
from p_os import Cmd
from p_mysql import Database
from p_client import Client
misc = Misc()
cmd = Cmd()
db = Database()
client = Client()

class Service(object):
    def checkServiceStatusWithOffline(self,id):
        result = self.getService('attri','name,status',id)
        if result['ret'] == 0:
            if result['output'][0][1] == 0:
                ret = {"ret":0,"output":"Service %s is offline." % result['output'][0][0]}
            else:
                ret = {"ret":-1,"output":"Service %s is online." % result['output'][0][0]}
        else:
            ret = {"ret":-1,"output":"Failed to get service status"}
        return ret
    def getService(self,cate,key=None,id=None):
        if cate == 'list':
            sql = "select id,name,descrip from service;"
        elif cate == 'attri':
            sql = "select %s from service where id=%s;" % (key,id)
        return db.mysql(sql)
    def post1(self,data):
        ret = misc.keycheck(data,'name,descrip,is_public,is_for_tc,command,critical,envcmd')
        if ret:
            return json.dumps(ret)
        if data['is_for_tc'] == 1:
            ret = misc.keycheck(data,'task_console,task_result,task_status,task_logpath,task_stop')
            if ret:
                return json.dumps(ret)           
            sql = "insert into service values (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (data['name'],data['descrip'],data['is_public'],data['is_for_tc'],data['command'],0,data['critical'],data['task_console'],data['task_result'],data['task_status'],data['task_logpath'],data['task_stop'])
        else: 
            sql = "insert into service values (NULL,'%s','%s','%s','%s','%s','%s','%s',NULL,NULL,NULL,NULL,NULL);" % (data['name'],data['descrip'],data['is_public'],data['is_for_tc'],data['command'],0,data['critical'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to add service %s with service_id:%s" % (data['name'],result['output'])}
        else:
            ret = {"ret":-1,"output":"Failed to add service %s as reason [%s]" % (data['name'],result['output'])}           
        return json.dumps(ret)
    def post(self,data):
        ret = misc.keycheck(data,'name,descrip,is_public,is_for_tc,command,critical,envcmd,task_console,task_result,task_status,task_logpath,task_stop')
        if ret:
            return json.dumps(ret)      
        sql = "insert into service (name,descrip,is_public,is_for_tc,command,status,critical,envcmd,task_console,task_result,task_status,task_logpath,task_stop) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (data['name'],data['descrip'],data['is_public'],data['is_for_tc'],data['command'],0,data['critical'],data['envcmd'],data['task_console'],data['task_result'],data['task_status'],data['task_logpath'],data['task_stop'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to add service %s with service_id:%s" % (data['name'],result['output'])}
        else:
            ret = {"ret":-1,"output":"Failed to add service %s as reason [%s]" % (data['name'],result['output'])}           
        return json.dumps(ret)        
    def delete(self,data):
        ret = misc.keycheck(data,'id')
        if ret:
            return json.dumps(ret)
        id = data['id']
        ## think about if need check task is running
        sql = 'delete from driver where service_id=%s;,,,delete from parameter where service_id=%s;,,,delete from envfile where service_id=%s;,,,delete from service where id=%s' % (id,id,id,id)
        result = db.mysql(sql)
        print result
        print sql
        if isinstance(result,dict):
            ret = {"ret":-1,"output":"Failed to delte service as reason %s" % result['output']}
        else:
            ret = {"ret":0,"output":"Successful to delete service."} 
        return json.dumps(ret)
    def put(self,data):
        ret = misc.keycheck(data,'id,name,descrip,is_public,is_for_tc,command,status,critical,envcmd,task_console,task_result,task_status,task_logpath,task_stop')
        if ret:
            return json.dumps(ret)        
        sql = "update service set name='%s',descrip='%s',is_public=%s,is_for_tc=%s,command='%s',status=%s,critical=%s,envcmd='%s',task_console='%s',task_result='%s',task_status='%s',task_logpath='%s',task_stop='%s' where id=%s" % (data['name'],data['descrip'],data['is_public'],data['is_for_tc'],data['command'],data['status'],data['critical'],data['envcmd'],data['task_console'],data['task_result'],data['task_status'],data['task_logpath'],data['task_stop'],data['id'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to update service %s." % data['name']}
        else:
            ret = {"ret":0,"output":"Failed to update service %s as reason [%s]." % (data['name'],result['output'])}
        return json.dumps(ret)
    def get(self,data):
        ret = misc.keycheck(data,'cate')
        if ret:
            return json.dumps(ret)        
        if data['cate'] == 'attri':
            ret = misc.keycheck(data,'key,id')
            if ret:
                return json.dumps(ret)
            sql = "select %s from service where id=%s;" % (data['key'],data['id'])
            result = self.getService(data['cate'],data['key'],data['id'])
        else:
            sql = "select id,name,descrip from service;"
            result = self.getService(data['cate'])
        if not result['output']:
            result = {"ret":0,"output":{}}
        else:
            result = db.returnJsonWhenGet(sql,result['output'])
        return json.dumps(result)
class Driver(Service):
    def taskCount(self,driver_id,type):
        #type could be get/update,update will do more opreations
        sql = "select count(id) from task where driver_id=%s where status in (1,2,5);" % driver_id
        result = db.mysql(sql)
        if result['ret'] == 0:
            count = result['output'][0][0]
            if type == 'get':
                ret = {"ret":0,"output":count}
            else:
                sql = "update driver set task_count=%s where id=%s;" % (count,driver_id)
                result = db.mysql(sql)
                if result['ret'] == 0:
                    ret = {"ret":0,"output":"Successful to update task count for driver"}
                else:
                    ret = {"ret":-1,"output":"Failed to update task count for driver as reason [%s]" % result['output']}
        else:
            ret = {"ret":-1,"output":"Failed to get task count for driver as reason [%s]" % result['output']}
        return ret
    def post(self,data):
        ret = misc.keycheck(data,'name,user,password,site,service_id')
        if ret:
            return json.dumps(ret)
        name = data['name']
        user = data['user']
        password = data['password']
        result = cmd.setupAuth(name,user,password,'pact')
        if result['ret' ] == 0:
            res,output = commands.getstatusoutput('scp -p /pact/etc/file/pact_driver %s:/usr/bin/' % name)
            if not os.path.exists(r'/pact/etc/pubkey/%s.pubkey' % name):
                genpub = cmd.rexec(name,'root','nop','[ ! -f /root/.ssh/id_rsa ] && echo y|ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa')
                res1,output1 = commands.getstatusoutput('scp -p %s:/root/.ssh/id_rsa.pub /pact/etc/pubkey/%s.pubkey' % (name,name))
            else:
                genpub = {"ret":0}
                res1 = 0
            if -1 in [res,genpub['ret'],res1]:
                ret = {"ret":-1,"output":"Failed to add driver node %s as reason [%s,%s,%s]" % (name,output,genpub['output'],output2)}
            else:
                ip = misc.getIPByHost(data['name'])['output']
                sql = "insert into driver values (NULL,'%s','%s','%s','%s','%s','%s','%s','%s');" % (name,ip,user,password,1,data['site'],0,data['service_id'])
                result = db.mysql(sql)
                if result['ret'] == 0:
                    ret = {"ret":0,"output":"Successful to add driver node %s with driver_id:%s" % (name,result['output'])}
                else:
                    ret = {"ret":-1,"output":"Failed to add driver node %s as reason [%s]" % (name,result['output'])}
        else:
            ret = {"ret":-1,"output":"Failed to add driver node %s as reason [%s]" % (name,result['output'])}
        return json.dumps(ret)
    def delete(self,data):
        ret = misc.keycheck(data,'id,name,service_id') 
        if ret:
            return json.dumps(ret) 
        result = self.checkServiceStatusWithOffline(data['service_id'])
        if result['ret'] == -1:
            return json.dumps(result)
        sql = "delete from driver where id=%s;" % data['id']
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to delete driver %s" % data['name']}
        else:
            ret = {"ret":-1,"output":"Failed to delete driver %s" % data['name']}
        return json.dumps(ret)
    def put(self,data):
        ret = misc.keycheck(data,'name,user,password,status,site,id,service_id')
        if ret:
            return json.dumps(ret)
        result = self.checkServiceStatusWithOffline(data['service_id'])
        if result['ret'] == -1:
            return json.dumps(result)        
        sql = "update driver set name='%s',user='%s',password='%s',status='%s',site='%s' where id=%s;" % (data['name'],data['user'],data['password'],data['status'],data['site'],data['id'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to update driver %s" % data['name']}
        else:
            ret = {"ret":-1,"output":"Failed to update driver %s" % data['name']}
        return json.dumps(ret)
    def get(self,data):
        ret = misc.keycheck(data,'service_id')
        if ret:
            return json.dumps(ret)
        #self.taskCount(data['id'],'update')
        sql = "select * from driver where service_id=%s;" % data['service_id']
        result = db.mysql(sql)
        if result['ret'] == -1:
            ret = json.dumps(result)
        elif not result['output']:
            ret = {"ret":0,"output":{}}
        else:
            ret = db.returnJsonWhenGet(sql,result['output'])
        return json.dumps(ret)
class Parameter(Service):
    def getOptionValue(self,user_id,option,value):
        if re.match(r'^cmd:',value):
            cmd = value.split('cmd:')[1]
            driver = db.mysql("select ip from driver where service_id=%s and status=1;" % service_id)
            if driver['ret'] == -1 or not driver['output']:
                ret = {"ret":-1,"output":"Failed to get default value sets for option %s as reason [driver:%s]" % (option,driver['output'])}
                return ret
            else:
                ip = driver['output']
                values = cmd.rexec(ip,'root','nop',cmd)
                if values['ret'] == -1 or not values['output']:
                    ret = {"ret":-1,"output":"Failed to get default value sets for option %s as reason [values:%s]" % (option,values['output'])}
                    return ret
                else:
                    values['output'] = re.sub(r'\n{1,}|\s{1,}',',',values['output'])
                    return values
        elif re.match(r'^api:',value):
            apiname = value.split('api:')[1]
            if apiname == 'getNode':
                return client.getNode(user_id)
        else:
            return value.split('s:')[1]
    def post(self,data):
        ret = misc.keycheck(data,'name,value,is_necessary,service_id')
        if ret:
            return json.dumps(ret)
        value = data['value']
        if not re.match(r'^cmd:|^api:|^static:',value):
            ret = {"ret":-1,"output":"Failed to add parameter as reason [invalid default value sets]"}
            return json.dumps(ret)
        sql = "insert into parameter values (NULL,'%s','%s',%s,%s);" % (data['name'],data['value'],data['is_necessary'],data['service_id'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to add paramter '%s' with parameter_id:%s" % (data['name'],result['output'])}
        else:
            ret = {"ret":-1,"output":"Failed to add paramter '%s' as reason [%s] " % (data['name'],result['output'])}
        return json.dumps(ret)
    def delete(self,data):
        ret = misc.keycheck(data,'id,name,service_id')
        if ret:
            return json.dumps(ret) 
        result = self.checkServiceStatusWithOffline(data['service_id'])
        if result['ret'] == -1:
            return json.dumps(result)
        sql = "delete from parameter where id=%s;" % data['id']
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to delete parameter %s" % data['name']}
        else:
            ret = {"ret":-1,"output":"Failed to delete parameter %s as reason [%s]" % (data['name'],result['output'])}
        return json.dumps(ret)
    def put(self,data):
        ret = misc.keycheck(data,'id,name,value,is_necessary,service_id')
        if ret:
            return json.dumps(ret) 
        result = self.checkServiceStatusWithOffline(data['service_id'])
        if result['ret'] == -1:
            return json.dumps(result)   
        sql = "update parameter set name='%s',value='%s',is_necessary=%s where id=%s" % (data['name'],data['value'],data['is_necessary'],data['id'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to update parameter"}
        else:
            ret = {"ret":-1,"output":"Failed to update parameter as reason [%s]" % result['output']}
        return json.dumps(ret)        
    def get(self,data):
        ret = misc.keycheck(data,'type,service_id')
        if ret:
            return json.dumps(ret)
        type = data['type']
        service_id = data['service_id']
        if type == 'display':
            sql = "select id,name,value,is_necessary from parameter where service_id=%s" % service_id
            return db.get({"sql":sql})
        elif type == 'task':
            user_id = data['user_id']
            sql = "select name,value,is_necessary from parameter where service_id=%s" % service_id
            result = db.mysql(sql)
            if result['ret'] == -1:
                return json.dumps(result)
            elif not result['output']:
                ret = {"ret":-1,"output":{}}
                return json.dumps(ret)            
            else:
                output = result['output']
                j = 0
                for i in output:
                    value = getOptionValue(user_id,i[0],i[1])
                    if value['ret'] == -1:
                        return json.dumps(value)
                    else:
                        result['output'][j][1] = value['output']
                    j+=1
                return db.returnJsonWhenGet(sql,result['output'])
        else:
            ret = {"ret":-1,"output":"invalid type in parameter.get"}
            return json.dumps(ret)
class Envfile(Service):
    def getDefValue(self,data):
        value = data['value']
        if re.match(r'^cmd:',value):
            cmd = value.split('cmd:')[1]        
            replace_src = re.findall(r'_[A-Z0-9]+_','',cmd)
            if replace_src:
                replace_dst_key = re.findall(r'[A-Z0-9]+',replace_src).lower()
                length = len(replace_src)            
                for i in range(length):
                    ret = misc.keycheck(data,replace_dst_key[i])
                    if ret:
                        return ret                    
                    cmd = re.sub(replace_src[i],data[replace_dst_key[i]],cmd)
            driver = db.mysql("select ip from driver where service_id=%s and status=1;" % service_id)
            if driver['ret'] == -1 or not driver['output']:
                ret = {"ret":-1,"output":"Failed to get default value for envfile as reason [envfile:%s]" % (driver['output'])}
                return ret
            else:
                ip = driver['output']
                values = cmd.rexec(ip,'root','nop',cmd)
                if values['ret'] == -1 or not values['output']:
                    ret = {"ret":-1,"output":"Failed to get default value for for envfile as reason [envfile:%s]" % (driver['output'])}
                    return ret
                else:
                    values['output'] = re.sub(r'\n{1,}|\s{1,}',',',values['output'])
                    return values
        elif re.match(r'^api:',value):
            apiname = value.split('api:')[1]
            if apiname == 'getNode':
                return client.getNode(user_id)
        else:
            return value.split('s:')[1]    
    def post(self,data):
        ret = misc.keycheck(data,'file_path,content,service_id')
        if ret:
            return json.dumps(ret)
        if not re.match(r'^cmd:|^api:|^static:',value):
            ret = {"ret":-1,"output":"Failed to add envfile as reason [invalid default value sets]"}
            return json.dumps(ret)            
        sql = "insert into envfile (file_path,content,service_id) values ('%s','%s',%s);" % (data['file_path'],data['content'],data['service_id'])
        result = db.mysql(sql)
        if result['ret'] == -1:
            result['output'] = "Failed to add envfile template"
        return json.dumps(result)
    def delete(self,data):
        ret = misc.keycheck(data,'id,service_id')
        if ret:
            return json.dumps(ret) 
        result = self.checkServiceStatusWithOffline(data['service_id'])
        if result['ret'] == -1:
            return json.dumps(result)
        sql = "delete from parameter where id=%s;" % id
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to delete envfile"}
        else:
            ret = {"ret":-1,"output":"Failed to delete envfile"}
        return json.dumps(ret)
    def put(self,data):
        ret = misc.keycheck(data,'id,file_path,content')
        if ret:
            return json.dumps(ret) 
        result = self.checkServiceStatusWithOffline(data['service_id'])
        if result['ret'] == -1:
            return json.dumps(result)   
        sql = "update envfile set file_path='%s',content='%s',id='%s' where id=%s" % (data['file_path'],data['content'],data['id'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to update parameter"}
        else:
            ret = {"ret":-1,"output":"Failed to update parameter as reason [%s]" % result['output']}
        return json.dumps(ret)  
    def get(self,data):
        ret = misc.keycheck(data,'type,service_id')
        if ret:
            return json.dumps(ret)
        type = data['type']
        service_id = data['service_id']
        tc = data['tc']        
        if type == 'display':
            sql = "select file_path,content from envfile where service_id=%s" % service_id
            return db.get({"sql":sql})
        elif type == 'task':
            sql = "select file_path,content from envfile where service_id=%s" % service_id
            result = db.mysql(sql)
            if result['ret'] == -1:
                return json.dumps(result)
            elif not result['output']:
                ret = {"ret":-1,"output":{}}
                return json.dumps(ret)            
            else:
                output = result['output']
                data['value'] = output[1]
                value = getDefValue(data)
                if value['ret'] == -1:
                    return json.dumps(value)
                else:
                    result['output'][1] = value['output']
                return db.returnJsonWhenGet(sql,result['output'])            
        else:
            ret = {"ret":-1,"output":"invalid type in envfile.get"}
            return json.dumps(ret)
        