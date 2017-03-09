'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time

class Items(object):
    '''
    classdocs
    '''


    def __init__(self, item_to_verify, item_staging_value,item_existing_value,getstagefunc,getprodfunc):
        '''
        Constructor
        '''
        self.item_to_verify=item_to_verify
        self.item_staging_value=self.getstagingvalue()
        self.item_existing_value=item_existing_value
        self.getstagefunc=getstagefunc
        self.getprodfunc=getprodfunc
        
    def isthesame(self):
        pass
    
    def getstagingvalue(self):
        return self.getstagefunc()
    
    def getprodvalue(self):
        pass
    
    def __str__(self):
        return "item "+ self.item_to_verify + " item staging " + self.item_staging_value + " item existing value " + self.item_existing_value

     

def getixgbefunc():
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
    command="cat  /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'"
    #return connection.sendShell(command)
    return connection.run_Cmd(command)
     
item=Items('ixgbe','9000','8000',getixgbefunc,getixgbefunc)
print "item is " +  str(item)
print "item is the same : " + str (item.item_staging_value == item.item_existing_value)
print "ixgbe value is " + item.getstagingvalue().strip()

