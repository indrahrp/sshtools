'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time

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
        self.item_prod=getprodfunc
        self.item_existing_value=getexistfunc
        #self.getstagefunc=getstagefunc
        #self.getprodfunc=getprodfunc
        
    def isthesame(self):
        pass
    
    def getstagingvalue(self):
        return self.item_staging_value()
        #pass
    
    def getprodvalue(self):
        pass
    
    def __str__(self):
        return "item "+ self.item_to_verify + " item staging " + str(self.item_staging_value())+ " item existing value " + str(self.item_existing_value)

sshServer='sol1'
sshUsername='root'
sshPassword='changeme'
localstgdir='/var/tmp/stgdir/'


itemlist={
    'ixgbe':['sol1','na','local']
    }

#def gethostinfo('hostname'):
#    for host in itemlist:
        
print "itemlist " + str(itemlist['ixgbe'][1])
        
def getixgbefunc():
    
    if str(itemlist['ixgbe'][0]) == sshServer:
        print " check local directory"
        command="cat " +  localstgdir + "ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'"
    else:
        command="cat /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'"
        
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
        #return connection.sendShell(command)
    return connection.run_Cmd(command)


def getexistixgbefunc():
    
    
    command="cat /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'"
        
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
        #return connection.sendShell(command)
    return connection.run_Cmd(command)
     
item=Items('ixgbe',getixgbefunc,finit,getexistixgbefunc,finit)
print "item is " +  str(item)
print "item is the same : " + str (item.item_staging_value == item.item_existing_value)
#print "ixgbe value is " + item.getstagingvalue().strip()
print "ixgbe value is " + item.getstagingvalue()
