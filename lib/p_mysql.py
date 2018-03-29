import json,re
import MySQLdb
from p_misc import Misc
misc = Misc()

dbhost = '127.0.0.1'
dbuser = 'pact'
dbpassword = 'pact'
db = 'pact'

class Database(object):
    def restful(self,method,sql):
        sql = sql.lower()
        if method in sql:
            return None
        else:
            ret = {"ret":-1,"output":'Mismatch request method "%s" with sql sentence "%s"' % (method,sql)}
            return json.dumps(ret)
    def mysql(self,sql):
        #import pdb;pdb.set_trace()
        try:    
            sqlconnect = MySQLdb.connect(dbhost,dbuser,dbpassword,db)
            cursor = sqlconnect.cursor()
        except:
            ret = {"ret":-1,"output":"Failed to connect database"}
            return json.dumps(ret)
        try:
            if not re.search(',,,',sql):
                sql_lower = sql.lower()
                res = cursor.execute(sql)
                if 'insert' in sql_lower:
                    res = int(sqlconnect.insert_id())                    
                elif 'select' in sql_lower or 'desc' in sql_lower:
                    res = cursor.fetchall()
                sqlconnect.commit()
                ret = {"ret":0,"output":res}
                return ret
            else:
                output = []
                for i in sql.split(',,,'):
                    sql_lower = i.lower()
                    res = cursor.execute(i)
                    if 'insert' in sql_lower:
                        res = sqlconnect.insert_id()
                    elif 'select' in sql_lower:
                        res = cursor.fetchall()
                    ret = {"ret":0,"output":res}
                    output.append(ret)
                sqlconnect.commit()
                return output
        except Exception as e:
            ret = {"ret":-1,"output":str(e)}
            return ret
        finally:
            sqlconnect.close()
    def returnJsonWhenGet(self,sql,output):
        sqllist = sql.split(' ')
        if sqllist[1] == '*':
            sql0 = "desc %s" % sqllist[3]
            keys = [i[0] for i in self.mysql(sql0)['output']]
        else:
            keys = sqllist[1].split(',')
        colcount = len(keys)
        outputlist = []
        for i in output:
            rowdict = {}
            for j in range(colcount):
                rowdict[keys[j]] = i[j]
            outputlist.append(rowdict)
        ret = {"ret":0,"output":outputlist}
        return ret
    def post(self,data):
        ret = misc.keycheck(data,'sql')
        if ret:
            return json.dumps(ret)
        ret = self.restful('insert',data['sql'])
        if ret:
            return ret
        return json.dumps(self.mysql(data['sql']))
    def delete(self,data):
        ret = misc.keycheck(data,'sql')
        if ret:
            return json.dumps(ret)  
        ret = self.restful('delete',data['sql'])
        if ret:
            return ret    
        return json.dumps(self.mysql(data['sql']))
    def put(self,data):
        ret = misc.keycheck(data,'sql')
        if ret:
            return json.dumps(ret)
        ret = self.restful('update',data['sql'])
        if ret:
            return ret    
        return json.dumps(self.mysql(data['sql']))
    def get(self,data):
        ret = misc.keycheck(data,'sql')
        if ret:
            return json.dumps(ret)
        sql = re.sub(r"\s+"," ",data['sql'])
        ret = self.restful('select',sql)
        if ret:
            return ret
        result = self.mysql(sql)
        if result['ret'] == -1:
            return json.dumps(result)
        elif not result['output']:
            ret = {"ret":0,"output":{}}
            return json.dumps(ret)
        else:
            ret = self.returnJsonWhenGet(sql,result['output'])
            return json.dumps(ret)
