import commands,re
import json
import paramiko
class Cmd(object):
    def lexec(self,cmd):
        ret,output = commands.getstatusoutput(cmd)
        if ret != 0:
            ret = -1
        ret = {"ret":ret,"output":output}
        return ret
    def rexec(self,host,user,password,cmds,timeout=None):
        #cmds is one command or multi commands seperated by ,
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        #import pdb;pdb.set_trace()
        try:
            if timeout == None:
                ssh.connect(hostname=host,username=user,password=password)
            else:
                ssh.connect(hostname=host,username=user,password=password,timeout=timeout)
            if not re.match(',,,',cmds):               
                stdin,stdout,stderr = ssh.exec_command(cmds)
                ret = stdout.channel.recv_exit_status()
                if ret == 0:
                    info = stdout.read()
                else:
                    ret = -1
                    info = stderr.read()
                output = {"ret":ret,"output":info}
            else:
                output = []
                for cmd in cmds.split(',,,'):
                    stdin,stdout,stderr = ssh.exec_command(cmd)
                    ret = stdout.channel.recv_exit_status()
                    if ret == 0:
                        info = stdout.read()
                    else:
                        ret = -1
                        info = stderr.read()
                    output.append({"ret":ret,"output":info})
            return output
        except Exception as e:
            ret = {"ret":-1,"output":str(e)}
            return ret
        finally:
            ssh.close()
    def setupAuth(self,target,user,password,sources):
        cmds = []
        pubkeypath = '/pact/etc/pubkey'
        for source in sources.split(','):
            cmd = "cat %s/%s.pubkey" % (pubkeypath,source)
            ret = self.lexec(cmd)
            if ret['ret'] == 0:
                cmd0 = 'echo "%s" >> ~/.ssh/authorized_keys' % ret['output']
                cmds.append(cmd0)
            else:
                ret = {"ret":-1,"output":"Missing pubkey file for source %s" % source}
                return ret
        cmds = ',,,'.join(cmds)
        output = self.rexec(target,user,password,cmds,60)
        if isinstance(output,list):
            if -1 in [i['ret'] for i in output]:
                ret = {"ret":-1,"output":"Failed to setup user equivalence for reason [%s]" % output['output']}
            else:
                ret = {"ret":0,"output":"Finished to setup user equivalence from %s to %s" % (sources,target)}
        else:
            if output['ret'] == -1:
                ret = {"ret":-1,"output":"Failed to setup user equivalence for reason [%s]" % output['output']}
            else:
                ret = {"ret":0,"output":"Finished to setup user equivalence from %s to %s" % (sources,target)}
        if ret['ret'] == 0 and self.rexec(target,user,'nop','hostname',60)['ret'] == -1:
            ret = {"ret":-1,"output":"Failed to setup user equivalence from %s to %s" % (sources,target)}
        return ret