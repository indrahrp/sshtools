'''
Created on Mar 6, 2017

@author: UC205955
'''
import threading, paramiko,time
#from scp import SCPClient
 
class Ssh:
    shell = None
    client = None
    transport = None
 
    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        #self.transport = paramiko.Transport((address, 22))
        #self.transport.connect(username=username, password=password)
        print "connection is done"
 
        #thread = threading.Thread(target=self.process)
        #thread.daemon = True
        #thread.start()
 
    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()
 
    def openShell(self):
       
        self.shell = self.client.invoke_shell()
        print "shell invoked"
        time.sleep(1)
        self.__retrieveResp()
            #strdata = str(alldata)
            #strdata.replace('\r', '')
            #print unicode(strdata)
                
    def __retrieveResp(self):   
        
    
        alldata= ''
        while not alldata.endswith(':~# ') and not alldata.endswith('$ ') and not 'assword' in alldata:
        #while not alldata.endswith('$'):
            time.sleep(1)
            if self.shell.recv_ready():
                resp=self.shell.recv(1024)
                alldata += resp
                print "in" + resp
            else:
                print "cnt"
        
        return alldata
 
    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
            print "command is submitted "
            time.sleep(1)
            return self.__retrieveResp()
            
     
        else:
            print("Shell not opened.")
    
    
    
    def openShellsudo(self):
       
        self.shell = self.client.invoke_shell()
        print "shell invoked"
        time.sleep(1)
        self.__retrieveRespsudo()
            #strdata = str(alldata)
            #strdata.replace('\r', '')
            #print unicode(strdata)
                
    def __retrieveRespsudo(self):   
        
    
        alldata= ''
        while not alldata.endswith(':~# ') and not alldata.endswith('$ ') and not 'assword' in alldata and not alldata.endswith('} ') and not alldata.endswith('Subject: ') and not alldata.endswith('EOT '):
        #while not alldata.endswith('$'):
            time.sleep(1)
            if self.shell.recv_ready():
                resp=self.shell.recv(1024)
                alldata += resp
                print "in" + resp
            else:
                print "cnt"
        
        return alldata
 
    def sendShellsudo(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
            print "command is submitted "
            time.sleep(1)
            return self.__retrieveRespsudo()
            
     
        else:
            print("Shell not opened.")
    
    
    
    
    
    def run_Cmd(self,cmd):
        print "run command :  " + cmd
        stdin,stdout,stderr=self.client.exec_command(cmd)
        #time.sleep(1)
        output = stdout.read()
        errs= stderr.read()
        #for out  in  output:
        #    print out   
        #if stderr:
        #    for line in stderr:
        #        print line.strip('\n')
        #    return stderr
        
        #for line in stderr: 
        #    print line.strip('\n')  
        
        
        #for line in stdout: 
        print "stderr : \n " + errs
        print "stdout : \n" +  output  
        return output


    def run_Cmd_stderr(self,cmd):
        print "run command : " + cmd
        stdin,stdout,stderr=self.client.exec_command(cmd)
        output = stdout.read()
        errs= stderr.read()
        #for out  in  output:
        #    print out   
        #if stderr:
        #    for line in stderr:
        #        print line.strip('\n')
        #    return stderr
        
        #for line in stderr: 
        #    print line.strip('\n')  
        
        
        #for line in stdout: 
        print "stderr : \n" + errs
        print "stdout : \n" +  output  
        return output,errs


    def run_Cmd_stderr1(self,cmd):
        print "run command : " + cmd
        stdin,stdout,stderr=self.client.exec_command(cmd)
        output = stdout.read()
        errs= stderr.read() 
        print "stderr : \n" + errs
        #print "stdout : \n" +  output  
        return output,errs
       
# SCPCLient takes a paramiko transport as its only argument
    def scpget(self,remotepath,localpath='',recursive=True):
        scpact = SCPClient(self.client.get_transport())
        scpact.get(remotepath,localpath)
        #scpact.get('testf')
        #else:
        #    print "incorrect argument"
        #exit(-1)
        scpact.close()
        print "scp done"
 
#connection = Ssh(sshServer, sshUsername, sshPassword)
#connection.run_Cmd('ls -lR /usr')
#connection.openShell()
#time.sleep(3)
#command='cat  /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#'
#connection.sendShell(command)
 

