import re
import json
class Usage(object):
    def getModule(self,data):
        module = []
        mods = dir(self)
        for mod in mods:
            if not re.search(r"^__|getModule",mod):
                module.append(mod)
        ret = {"ret":0,"output":module}
        return json.dumps(ret)
    def Database(self,data):
        usage = 'GET: {"target":"Usage","module":"Database"} to get usage of Database:\n\n\nUsage:\nPOST: {"target":"Database","sql":"SQL"}\nDELETE: {"target":"Database","sql":"SQL"}\nPUT: {"target":"Database","sql":"SQL"}\nGET: {"target":"Database","sql":"SQL"}'
        return usage
    def User(self,data):
        usage = 'GET: {"target":"Usage","module":"User"} to get usage of User:\n\n\nUsage:\nPOST: {"target":"User","username":username,"password":password,"email":email,"pool":pool}\nDELETE: {"target":"User","id":id}\nPUT: {"target":"User","action":"updaterole","userid":userid,"level":level,"service_id":service_id},{"target":"User","action":"updateprofile","username":username,"password":password,"status":status,"pool":pool,"id":id},{"target":"User","action":"auth","username":username,"password":password},{"target":"User","action":"ldap_auth","username":username,"password":password},{"target":"User","action":"login","username":username,"password":password}\nGET: {"target":"User"},{"target":"User","id":id}'
        return usage
    def Event(self,data):
        usage = 'GET: {"target":"Usage","module":"Event"} to get usage of Event:\n\n\nUsage:\nPOST: {"target":"Event","level":level,"content":content}\nGET: {"target":"Event"}'
        return usage
    def Service(self,data):
        usage = 'GET: {"target":"Usage","module":"Service"} to get usage of Service:\n\n\nUsage:\nPOST:{"target":"Service","name":name,"descrip":descrip,"is_for_tc":is_for_tc,"command":command,"critical":critical,"tc_console":tc_console,"tc_result":tc_result,"tc_status":tc_status,"tc_logpath":tc_logpath,"tc_stop":tc_stop}\nDELETE: {"target":"Service","id":id}\nPUT: {"target":"Service","id":id,"name":name,"descrip":descrip,"is_public":is_public,"is_for_tc":is_for_tc,"command":command,"status":status,"critical":critical,"tc_console":tc_console,"tc_result":tc_result,"tc_status":tc_status,"tc_logpath":tc_logpath,"tc_stop":tc_stop}\nGET: {"target":"Service","cate":"list"},{"target":"Service","cate":"attri","key":key,"id":id}'
        return usage
    def Driver(self,data):
        usage = 'GET: {"target":"Usage","module":"%s"} to get usage of %s:\n\n\nUsage:\nPOST: {"target":"%s","name":name,"user":user,"password":password,"site":site,"service_id":service_id}\nDELETE: {"target":"%s","id":id,"name":name,"service_id":service_id}\nPUT: {"target":"%s","name":name,"user":user,"password":password,"status":status,"site":site,"id":id,"service_id":service_id}\nGET: {"target":"%s","service_id":service_id}' % (data['module'],data['module'],data['module'],data['module'],data['module'],data['module'])
        return usage
    def Parameter(self,data):
        usage = 'GET: {"target":"Usage","module":"%s"} to get usage of %s:\n\n\nUsage:\nPOST: {"target":"%s","name":name,"value":value,"is_necessary":is_necessary,"service_id":service_id}\nDELETE: {"target":"%s","id":id,"name":name,"service_id":service_id}\nPUT: {"target":"%s","id":id,"name":name,"value":value,"is_necessary":is_necessary,"service_id":service_id}\nGET: {"target":"%s","type":"display","service_id":service_id},{"target":"%s","type":"task","user_id":user_id,"service_id":service_id}' % (data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'])
        return usage    
    def Envfile(self,data):
        usage = 'GET: {"target":"Usage","module":"%s"} to get usage of %s:\n\n\nUsage:\nPOST: {"target":"%s","file_path":file_path,"content":content,"service_id":service_id}\nDELETE: {"target":"%s","id":id,"service_id":service_id}\nPUT: {"target":"%s","id":id,"file_path":file_path,"content":content,}\nGET: {"target":"%s","type":type,"service_id":service_id}' % (data['module'],data['module'],data['module'],data['module'],data['module'],data['module'])
        return usage  
    def Pool(self,data):
        usage = 'GET: {"target":"Usage","module":"%s"} to get usage of %s:\n\n\nUsage:\nPOST: {"target":"%s","name":name,"descrip":descrip}\nDELETE: {"target":"%s","id":id,"name":name}\nPUT: {"target":"%s","id":id,"name":name,"descrip":descrip,}\nGET: {"target":"%s"}' % (data['module'],data['module'],data['module'],data['module'],data['module'],data['module'])
        return usage      
    def Site(self,data):
        usage = 'GET: {"target":"Usage","module":"%s"} to get usage of %s:\n\n\nUsage:\nPOST: {"target":"%s","name":name,"descrip":descrip}\nDELETE: {"target":"%s","id":id,"name":name}\nPUT: {"target":"%s","id":id,"name":name,"descrip":descrip,}\nGET: {"target":"%s"}' % (data['module'],data['module'],data['module'],data['module'],data['module'],data['module'])
        return usage
    def Client(self,data):
        usage = 'GET: {"target":"Usage","module":"%s"} to get usage of %s:\n\n\nUsage:\nPOST: {"target":"%s","name":name,"user":user,"password":password,"pool":pool,"site":site,"clus_flag":clus_flag,"user_id":user_id}\nDELETE: {"target":"%s","id":id,"name":name}\nPUT: {"target":"%s","type":"profile","id":id,"name":name,"user":user,"password":password,"status":status,"site":site,"clus_flag":clus_flag},{"target":"%s","type":"ownership","id":id,"pool":pool,"user_id":user_id},{"target":"%s","type":"taskid","id":id,"name":name,"task_id":task_id},{"target":"%s","type":"status","id":id,"name":name},{"target":"%s","type":"setAuth","id":id,"name":name}\nGET: {"target":"%s","type":"list"},{"target":"%s","type":"attri","id":id},{"target":"%s","type":"nodeForUser","user_id":user_id}' % (data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'],data['module'])
        return usage        