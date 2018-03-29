import ldap
import json
import sys
from p_misc import Misc
from p_mysql import Database
misc = Misc()
db = Database()

class User(object):
    def __init__(self):    
        self.ldapserver = 'ldap://vldap-prod.community.veritas.com:389'
        self.domain = 'community'
    def getUser(self):
        sql = "select id,username,email,status from user;"
        data = {"sql":sql}
        return eval(db.get(data))
    def getUserDetail(self,id):      
        sqls = ["select * from user where id=%s;" % id,"select user_group.group_id,service.id,service.name from user_group inner join service on user_group.service_id=service.id and user_group.user_id=%s;" % id]
        result = db.get({"sql":sqls[0]})
        result = eval(result)
        ugout = db.mysql(sqls[1])
        if ugout['output']:
            if 1 in [i[0] for i in ugout['output']]:
                result['output']['role'] = {"0":{"level":"system","module":"any"}}
            else:
                result['output']['role'] = {}
                seq = 0
                for i in ugout['output']:
                    result['output']['role']['seq']={"level":"admin","module":i[2]}
                    sql +=1
        return result
    def auth_ldap(self,username,password):
        domainusername = self.domain + '\\' + username  
        try:
            conn = ldap.initialize(self.ldapserver)
            conn.simple_bind_s(domainusername,password)
            ret = {"ret":0,"output":"Authorization by ldap is passed"}
        except:
            ret = {"ret":-1,"output":"Authorization by ldap is failed"}
        return ret
    def auth_password(self,username,password):
        password = misc.md5(password)      
        sql = "select count(id) from user where username='%s' and password='%s';" % (username,password)
        result = db.mysql(sql)
        if result['ret'] == 0 and result['output'][0][0] == 1:
            ret = {"ret":0,"output":"Authorization by local password is passed"}
        else:
            ret = {"ret":-1,"output":"Authorization by local password is failed"}
        return ret          
    def auth0(self,username,password):
        sql = "select login_by_ldap from setting;"
        result = db.mysql(sql)
        if result['ret'] == 0:
            if result['output'][0][0] == 1:
                return self.autch_ldap(username,password)
            else:
                return self.auth_password(username,password)
        else:
            ret = {"ret":-1,"output":"Failed to get authentication method"}
            return ret
    def auth(self,username,password):
        result = self.auth_password(username,password)
        if result['ret'] == -1:
            result = self.auth_ldap(username,password)
            if result['ret'] == -1:
                result = {"ret":-1,"output":"Authorization by local password or ldap is failed"}
        return result
    def login(self,username,password):
        ret = ''
        sql = "select count(id) from user where username='%s';" % username
        result = db.mysql(sql)
        if result['ret'] == -1:
            ret = result['output']
        else:
            if result['output'][0][0] == 0:
                ret = {"ret":-1,"output":"Username %s doesn't exist,please register first" % username}
        if ret:
            return ret
        ret = self.auth(username,password)
        if ret['ret'] == 0:
            login_date = misc.gettime('timestamp')
            sql = "update user set login_date='%s' where username='%s';" % (login_date,username)
            result = db.mysql(sql)
            if result['ret'] == 0:
                ret = {"ret":0,"output":"Login check is passed"}
            else:
                ret = {"ret":0,"output":"Login check is passed,but failed to update login date"}
        return ret
    def checkUser(self,username,email):
        ret = ''
        sql = "select count(id) from user where username='%s' or email='%s';" % (username,email)
        result = db.mysql(sql)
        if result['ret'] == 0:
            if result['output'][0][0] == 1:
                ret = {"ret":-1,"output":"Please check the username/email you input as the record is found in pact."}
        else:
            ret = {"ret":-1,"output":"Faield to check if username/email exists in pact."}
        if ret:
            return json.dumps(ret)
    def updateProfile(self,data):
    #data is a dict which should have key:username,password,status,id
        ret = self.checkUser(data['username'],data['email'])
        if ret:
            return ret
        sql = "update user set username='%s',password='%s',status=%s,pool=%s where id=%s;" % (data['username'],misc.md5(data['password']),data['status'],data['pool'],data['id'])
        return db.mysql(sql)
    def updateRole(self,userid,level,service_id=None):
        if level == 'system':
            sqls = ["delete from user where user_id=%s;" % userid,"insert into user_group values (NULL,%s,'system',0);" % userid]
        else:
            sqls = ["delete from user where user_id=%s;" % userid]
            for i in service_id.split(','):
                sql = "insert into user_group values (NULL,%s,'admin',0);" % userid
                sqls.append(sql)
        result = db.mysql(sqls)
        if result['ret'] == 0:
            ret = {"ret":0,"output":"Successful to update Role."}
        else:
            ret = {"ret":-1,"output":"Faield to update Role as reason %s." % result['output']}
        return ret
    def post(self,data):
        ret = misc.keycheck(data,'username,password,email,pool')
        if ret:
            return json.dumps(ret)
        ret = self.checkUser(data['username'],data['email'])
        if ret:
            return ret
        reg_date = misc.gettime('timestamp')
        sql = "insert into user value (NULL,'%s','%s','%s',1,1,%s,'%s','%s');" % (data['username'],misc.md5(data['password']),data['email'],data['pool'],reg_date,reg_date)
        result = db.mysql(sql)
        if result['ret'] == 0:
            result = {"ret":0,"output":"Successful to add user %s." % data['username']}
        else:
            result = {"ret":-1,"output":"Failed to add user %s as reason [%s]." % (data['username'],result['output'])}
        return json.dumps(result)
    def delete(self,data):
        ret = misc.keycheck(data,'id')
        if ret:
            return ret
        sql = "update user set status=0 where id='%s';" % data['id']
        return json.dumps(db.mysql(sql))
    def put(self,data):
        ret = misc.keycheck(data,'action')
        if ret:
            return json.dumps(ret)
        if data['action'] == 'updaterole':
            ret = misc.keycheck(data,'userid,level,service_id')
            if ret:
                return json.dumps(ret)
            result = self.updateRole(data['userid'],data['level'],data['service_id'])
        else:
            ret = misc.keycheck(data,'username,password')
            if ret:
                return json.dumps(ret)
            if data['action'] == 'updateprofile':
                ret = misc.keycheck(data,'status,pool,id')
                if ret:
                    return json.dumps(ret)
                result = self.updateProfile(data)          
            elif data['action'] == 'auth':
                result = self.auth(data['username'],data['password'])
            elif data['action'] == 'ldap_auth':
                result = self.auth_ldap(data['username'],data['password'])
            elif data['action'] == 'login':
                result = self.login(data['username'],data['password'])
            else:
                result = {"ret":-1,"output":"Invalid action for User.post"}
        return json.dumps(result)
    def get(self,data):
        if misc.keycheck(data,'id'):
            result = self.getUser()
        else:
            result = self.getUserDetail(data['id'])
        return json.dumps(result)      