'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
#from Scpapi import *
import time

class Items(object):
    '''
    classdocs to explain what it does again ...
    '''


    def __init__(self, toverify, stagingsvr,prodsvr,getstagefunc,getprodfunc):
        '''
        Constructor
        '''
        self.toverify=toverify
        self.stagingsvr=stagingsvr
        self.prodsvr=prodsvr
        self.getstagefunc=getstagefunc
        self.getprodfunc=getprodfunc
        
    def isthesame(self):
        pass
    
    def getstagingvalue(self):
        return self.getstagefunc(self.stagingsvr)
    
    def getprodvalue(self):
        return self.getprodfunc(self.prodsvr)
    
    def __str__(self):
        #return "item "+ self.toverify + " item staging " + self.value + " item existing value " + self.item_existing_value
        return 'test'

global sol1,sol2
sol1='192.168.56.10'
sol2='192.168.56.20'  
localhost='127.0.0.1'
sshUsername='root'
sshPassword='changeme'
workdir='c\:\temp\\'

def getixgbefunc(sshServer):
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
    command="cat  /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'"
    #return connection.sendShell(command)
    return connection.run_Cmd(command)
     
#item=Items('ixgbe',sol1,sol2,getixgbefunc,getixgbefunc)
#print "item is " +  str(item)
#print "item is the same : " + str (item.item_staging_value == item.item_existing_value)
#print "ixgbe value is " + item.getstagingvalue().strip()
#print "item is the same : " + str (item.item_staging_value == item.item_existing_value)
#print "ixgbe value is " + item.getprodvalue().strip()

def getusrpkg(sshServer):
    connection = Ssh(sshServer, sshUsername, sshPassword)
    command="/usr/pkg/sbin/pkg_info|sort > /var/tmp/pkginfo.txt"
    
    print "executing " + command
    connection.run_Cmd(command)
    pkgout='pkginfo'+ sshServer
    #localfile=workdir+pkgout
    localfile=pkgout
    connection.scpget('/var/tmp/pkginfo.txt',localfile)
    #connection.openShell()
    #return connection.sendShell(command)
    #return connection.run_Cmd(command)
def isthesame(stagesvr,prodsvr):
    
    connection = Ssh(localhost, sshUsername, sshPassword)
    command="/usr/pkg/sbin/pkg_info|sort > /var/tmp/pkginfo.txt"
    
    
    
item=Items('/usr/pkg',sol1,sol2,getusrpkg,getusrpkg,isthesame)
#print "/usr/pkg/ difference" + item.getstagingvalue()
item.getstagingvalue()

#print "/usr/pkg/ difference" + item.getprodvalue()
item.getprodvalue()