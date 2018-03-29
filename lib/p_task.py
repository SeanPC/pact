import json,re
from p_misc import Misc
from p_mysql import Database
misc = Misc()
db = Database()

#1: In Queue
#2: In Process
#3: Successful
#4: Failed
#5: Cancel
#6: Hold
#7: Unknown

class Task(object):
    def post(self,data):
        ret = misc.keycheck(data,'pid,is_release,service_id,driver_id,clients,user_id,start_time,end_time,os,kernel,product,state,envcmd,command')
        if ret:
            return json.dumps(ret)
        sql = "insert into task (pid,is_release,service_id,driver_id,clients,user_id,start_time,end_time,os,kernel,product,state,envcmd,command) values (data['pid'],data['is_release'],data['service_id'],data['driver_id'],data['clients'],data['user_id'],data['start_time'],data['end_time'],data['os'],data['kernel'],data['product'],data['state'],data['envcmd'],data['command']);"
        result = db.mysql(sql)
        if result['ret'] == 0:
            result['output'] = "Successful to create task with task_id:%s" % result['output']
        else:
            result['output'] = "Failed to create task as reason [%s]" % result['output']         
        return json.dumps(ret)
    def put(self,data):
        ret = misc.keycheck(data,'id,state')
        if ret:
            return json.dumps(ret)
        sql = "update task set state=%s where id=%s" % (data['state'],data['id'])
        result = db.mysql(sql)
        if result['ret'] == 0:
            result['output'] = "Successful to update task to state %s" % data['state']
        else:
            result['output'] = "Failed to update task state as reason [%s]" % result['output']         
        return json.dumps(ret)
    def get(self,data):
        ret = misc.keycheck(data,'key')
        if ret:
            return json.dumps(ret)        
        key = data['key']
        sql = "select %s from task;" % key
        return db.get({"sql":sql})