#!/usr/bin/env python
import importlib
import json
from lib import Misc

def router(data):
    ret = None
    if not isinstance(data,dict):
        ret = {"ret":-1,"output":"Input data is not dict"}
    elif 'target' not in data or 'method' not in data :
        ret = {"ret":-1,"output":"Missing keyword in dict,Need target and method"}
    elif not data['target'] or not data['method']:
        ret = {"ret":-1,"output":"Missing value of target and method"}
    if ret:
        return json.dumps(ret)

#if the module is usage,will display usage by call the method in p_doc.py        
    if data['target'] == 'Usage' and data['method'] == 'get':
        misc = Misc()
        ret = misc.keycheck(data,'module')
        if ret:
            method = 'getModule'
            ret = None
        else:
            method = data['module']
    else:
        method = data['method']
#dynamic imort and learn the method by defined under lib
    try:
        newmodule = importlib.import_module('lib')
        try:
            myclass = getattr(newmodule,data['target'])
            ins = myclass()
            try:
                mymethod = getattr(ins,method)
            except:
                ret = {"ret":-1,"output":"Undefied method %s for target %s" % (method,data['target'])}            
        except:
            ret = {"ret":-1,"output":"Undefined Target %s" % data['target']}
    except:
        ret = {"ret":-1,"output":"syntax error in python file under lib"}
    if ret:
        return json.dumps(ret)
    
 
    return mymethod(data)
    
    
    
if __name__ == '__main__':    
    import sys
    sys.path.append('/pact')
    #data = {"target":"user","action":"auth","username":"bentley.xu","password":"goouT860917@@"}
    #data = {"target":"Database","method":"get","sql":"select * from user"}
    data = {"target":"Usage","method":"get"}
    print router(data)
