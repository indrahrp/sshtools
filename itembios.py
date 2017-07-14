#!/usr/bin/env python

'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time,re,os,json,xml.etree.ElementTree
from scp import SCPClient
from paramiko import SSHClient,client
    


def finit():
    print "in finit"
    return "nothing"

class Items(object):
    '''
    classdocs
    '''


    def __init__(self, item_to_verify,getstagefunc=finit,getprodfunc=finit,getexistfunc=finit,verifyfunc=finit):
        '''
        Constructor
        '''
        self.item_to_verify=item_to_verify
        self.item_staging_value=getstagefunc
        self.item_prod_value=getprodfunc
        self.item_existing_value=getexistfunc
        self.item_verify_func=verifyfunc
        #self.getstagefunc=getstagefunc
        #self.getprodfunc=getprodfunc
        
    def isthesame(self):
        pass
    
    def getstagingvalue(self):
        return self.item_staging_value()
        #pass
    
    def getprodvalue(self):
        return self.item_prod_value()
 
    def getexistvalue(self):
        return self.item_existing_value()
 
    def get_verify(self):
        return self.item_verify_func()
    
    def __str__(self):
        return "item "+ self.item_to_verify + " item staging " + str(self.item_staging_value())+ " item existing value " + str(self.item_existing_value)




with open('config.json') as json_data_file:
    data = json.load(json_data_file)

print json.dumps(data, indent=4, sort_keys=True)
print "hostinfo host " + data["hostinfo"]["platform"]

sshServer=data["hostinfo"]["host"]
sshUsername=data["hostinfo"]["user"]

sshPassword=os.environ['SECRET']
stgdir=data["hostinfo"]["stgdir"]

print "pwd is "+ sshPassword

testl={'ixgbe':['satu','dua'],
       
       #'/etc/system':['dua','tiga']
       }
       
       #'dua'


print testl


connection = Ssh(sshServer, sshUsername, sshPassword)


    

def ReadFromFile(Filename):
    readfile=open(Filename,'r')
    result=readfile.read()
    return result

    
        
def get_stage_ixgbefunc():
    
    print "checking stage ixgbe.conf"
    command= "cat /var/tmp/stgdir/ixgbe.conf|sort|grep -v ^# | cksum| awk '{print $2}'"
    #command="cat " +  stgdir + "ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'|sed 's/default_mtu *=//'| sed 's/ *//'"
    
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and 'can not open' in error:
        print "file ixgbe.conf on staging does not exist"
        return False
    else:
        return output

def get_exist_ixgbefunc():
    
    print "checking existing ixgbe.conf "
    command= "cat /kernel/drv/ixgbe.conf|sort|grep -v ^#| cksum | awk '{print $2}'"
    
    #command="cat /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'|sed 's/default_mtu *=//'| sed 's/ *//'"
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file ixgbe.conf on existing system does not exist'
        return False
    else:
        return output
    
def verify_ixgbe():
  
    if item.getexistvalue() == item.getstagingvalue():
        return True
    else:
        return False
    
item=Items('ixgbe',get_stage_ixgbefunc,finit,get_exist_ixgbefunc,verify_ixgbe)
print "ixgbe.conf is the same as staging : " + str (item.get_verify()) 



def get_stage_system():
    print "check stage /etc/system"
    command="cat /var/tmp/stgdir/system|grep -v ^*|sort|grep -v ^$|cksum|awk '{print $2}'"
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file /etc/system on staging does not exist'
        return False
    else:
        return output.strip()

def get_exist_system():
    print "check existing /etc/system"
    command="cat /etc/system|grep -v ^*|sort|grep -v ^$|cksum | awk '{print $2}'"
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file /etc/system on existing system does not exist'
        return False
    else:
        return output.strip()
def verify_system():
  
    if item.getexistvalue() == item.getstagingvalue():
        return True
    else:
        return False
    
item=Items('system',get_stage_system,finit,get_exist_system,verify_system)
print "existing /etc/system is the same as staging : " +  str (item.get_verify())

def get_stage_sd():
    print "checking stage sd.conf "
    command="cat /var/tmp/stgdir/sd.conf|grep -v ^#|sort|grep -v ^$|cksum|awk '{print $2}'"
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file sd.conf on staging does not exist'
        return False
    else:
        return output.strip()

def get_exist_sd():
    print "checking  existing sd.conf"
    command="cat /kernel/drv/sd.conf|grep -v ^#|sort|grep -v ^$|cksum | awk '{print $2}'"
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file sd.conf on existing system does not exist'
        return False
    else:
        return output.strip()
def verify_sd():
  
    if item.getexistvalue() == item.getstagingvalue():
        return True
    else:
        return False
    
item=Items('system',get_stage_sd,finit,get_exist_sd,verify_sd)
print "existing /kernel/drv/sd.conf is the same as staging : " +  str (item.get_verify())




def get_stage_ndd():
    print "checking stage /etc/rc2.d/S68ndd "
    command="cat " +  stgdir + "S68ndd|egrep -vi '(^#|^$)'|sort | awk '{print $5}' |cksum|awk '{print $2}'"
    #connection.run_Cmd(command)
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file S68ndd from staging does not exist'
        return False
    else:
        return output.strip()
    
def get_exist_ndd():
    print "checking  existing /etc/rc2.d/S68ndd and what it is on the memory "
    command="cat /etc/rc2.d/S68ndd |sort|grep -v '^#'|grep -v '^$'|awk '{print $5}'|cksum|awk '{print $2}'"
    output,error=connection.run_Cmd_stderr(command)
    if output.strip()=='0' and ' cannot open' in error:
        print 'file S68ndd on existing system does not exist'
        return False
    
    command1="(cat /etc/rc2.d/S68ndd|egrep -vi '(^#|^$)'|sort| sed 's/-set/-get/'|sed 's/[0-9]*//g' > /tmp/s && bash /tmp/s|cksum | awk '{print $2}')"
    if output.strip() == connection.run_Cmd(command1).strip():
        return output.strip() 
    else:
        print "Existing /etc/rc2.d/S68ndd needs to be executed"
        return 0

item=Items('S68ndd',get_stage_ndd,finit,get_exist_ndd,finit)
print "existing /etc/rc2.d/S68ndd is the same as staging : " +  str (item.getstagingvalue() == item.getexistvalue())





def find_bios(biosfile,biosconfig=True):
    
    e = xml.etree.ElementTree.fromstring(biosfile) 
    if biosconfig:
        #e = xml.etree.ElementTree.fromstring(biosfile)
        hyperthread_iter=e.iter('Intel_R__HT_Technology').next()
        htset=hyperthread_iter.find('SELECTED_OPTION')
        print htset.text
        if htset.text.strip()=='0001':
            ht=True
            return ht
        else:
            return False
    else:
        turbo_mode=e.iter('Turbo_Mode').next()
        print "turbo_mode :" + turbo_mode.text
        
        UncoreFreq=e.iter('Uncore_Frequency_Scaling').next()
        print "Uncore Frequency : " + UncoreFreq.text

        EnergyPerf=e.iter('Energy_Performance').next()
        print "Energy Performance " + EnergyPerf.text

        hyperThread=e.iter('Hyper-threading').next()
        print "hyperThreading : " + hyperThread.text
        if (turbo_mode.text.strip() == 'Enabled' and UncoreFreq.text.strip() == 'Enabled' and EnergyPerf.text.strip() == 'Performance' and hyperThread.text.strip() == 'Enabled'):
            return True
        else:
            return False
  
    
   
         

def verify_bios():
    bios=True
    print " getting BIOS setting"
    connection = Ssh(sshServer, sshUsername, sshPassword)
    command="biosconfig -get_bios_settings > /var/tmp/biosconfig.txt"
    output,errs=connection.run_Cmd_stderr1(command)
    #print "bisoconfig  output" + output
    if 'is not supported' in errs:
        bios=False
        command="ubiosconfig export all > /var/tmp/biosconfig.txt"
        output,errs=connection.run_Cmd_stderr1(command)
        #print "ubisoconfig  output" + output
        if 'is not supported' in errs:
            print "biosconfig and ubiosconfig is not supported"
            return "Unable to Determine"
    
    command="cat /var/tmp/biosconfig.txt"
    output,errs=connection.run_Cmd_stderr1(command)
    return find_bios(output,bios)
    
item=Items('bios_setting',finit,finit,finit,verify_bios)
print "bios_setting is correct: " + str(item.get_verify())

def verify_sudo():
    print "verifying sudo \n login using user  " +  data["other"][data["hostinfo"]["server_env"]]["user_sudocheck"]
    
    sshUsername= data["other"][data["hostinfo"]["server_env"]]["user_sudocheck"]
    sshPassword= data["other"][data["hostinfo"]["server_env"]]["user_pwd"]
    connection1 = Ssh(sshServer, sshUsername, sshPassword)
    connection1.openShellsudo()
    #output=connection1.cmdtoShell('\n\n')
    output=connection1.cmdtoShell('sudo -l')

    print "output send cmdtoshell " + output

    if "assword" in output:
        output=connection1.cmdtoShell(sshPassword)
    print "output after sending password " + output
    if 'may run the following commands' in output:
        return True

#item=Items('sudo',finit,finit,finit,verify_sudo)
#print "sudo is working : " + str(item.get_verify())


def install_procmon():
    sshServer='192.168.56.10'
    print "installling procmon "   
    connection1 = Ssh(sshServer, sshUsername, sshPassword)
    connection1.openShellsudo()
    #output=connection1.cmdtoShell('\n\n')
    output=connection1.cmdtoShell("su - techsup;echo \n")

    print "output send cmdtoshell " + output
    
    command='/ilx/pmdist/sbin//distrib_procmon sol2'
    if ":techsup" in output:
        output=connection1.cmdtoShell(command)
        ##print "output after sending distibute command " + output
    
    command='/ilx/pmdist/sbin//distrib_rules sol2'
    if ":techsup" in output:
        output=connection1.cmdtoShell(command)
        ##print "output after sending distibute command " + output

install_procmon()

def install_monet():
    print "in scp client"
    print "copying Monet installation file"


    Username = "root"
    Password = "changeme"
    Server = "192.168.56.20"

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(client.AutoAddPolicy())
    ssh.connect(Server, username=Username, password=Password)
        
    # SCPCLient takes a paramiko transport as its only argument
    scp = SCPClient(ssh.get_transport())

    scp.put('6.125/Monet.6.125.solaris11.amd64.run', '/tmp/Monet.6.125.solaris11.amd64.run')
    #scp.get('/var/tmp/tdir','c:/temp',recursive=True)
    print "scp done"

    scp.close()
    
    print "executing Monet Install file"
    command="(chmod +x /tmp/Monet*;/tmp/Monet.6.125.solaris11.amd64.run)"
     
    output,error=connection.run_Cmd_stderr(command)
    #command="/tmp/Monet.6.125.solaris11.amd64.run)"
    #output,error=connection.run_Cmd_stderr(command)
    
    #if output.strip()=='0' and ' cannot open' in error:
    ##    print 'file sd.conf on existing system does not exist'
    #return False
    #else:
    # return output.strip()

install_monet()
