'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time,re

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
 
    
    def __str__(self):
        return "item "+ self.item_to_verify + " item staging " + str(self.item_staging_value())+ " item existing value " + str(self.item_existing_value)

sshServer='bunkerx1'
sshUsername='root'
sshPassword='changeme'
localstgdir='/var/tmp/stgdir/'


itemlist={
    'ixgbe':['sol1','na','local','']
    }

#def gethostinfo('hostname'):
#    for host in itemlist:
        
print "itemlist " + str(itemlist['ixgbe'][1])
        
def get_stage_ixgbefunc():
    
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


def get_exist_ixgbefunc():
    
    
    command="cat /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'"
        
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
        #return connection.sendShell(command)
    return connection.run_Cmd(command)
     
item=Items('ixgbe',get_stage_ixgbefunc,finit,get_exist_ixgbefunc,finit)
print "item is " +  str(item)
print "item is the same : " + str (item.getstagingvalue() == item.getexistvalue)
#print "ixgbe value is " + item.getstagingvalue().strip()
print "ixgbe staging value is " + item.getstagingvalue()
print "ixgbe existing value is " + item.getexistvalue()


def get_ht_setting():
    
    pass

def get_stage_system():
    print " check local directory"
    command="cat " +  localstgdir + "system|grep -v ^#|sort|grep -v ^$|cksum"
        
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
        #return connection.sendShell(command)
    return connection.run_Cmd(command)

def get_exist_system():
    print " check local directory"
    command="cat /etc/system|grep -v ^#|sort|grep -v ^$|cksum"
        
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
        #return connection.sendShell(command)
    return connection.run_Cmd(command)


item=Items('system',get_stage_system,finit,get_exist_system,finit)
print "item is " +  str(item)
#print "item is the same : " + str (item.getstagingvalue() == item.getexistvalue)
#print "ixgbe value is " + item.getstagingvalue().strip()
print "system staging value is " + item.getstagingvalue()
print "system existing value is " + item.getexistvalue()

def get_prod_mtu():
    print " getting previous prod mtu"
    fname='netstatii'
    fentry=ReadFromFile(fname)
    print "fentry  "+ fentry
    mtulist=find_mtu(fentry,'bunkerx1','tdn.pln.ilx.com')
    print "mtulist " + str(mtulist)
    return mtulist

def get_exist_mtu():
    print " getting current server mtu"
    command="netstat -i | grep -i " + sshServer
    connection = Ssh(sshServer, sshUsername, sshPassword)
    time.sleep(3)
    entry=connection.run_Cmd(command)
    print "entry " + entry
    return entry

def find_mtu(str1,svrname,domain):
    intlist=[]    
    Regex = re.compile(r'''
    (net\d+|ixgbe\d+|igb\d+|e1000g\d+)\s+(\d+)\s+''' + svrname + '''\.(\w+)\.''' + domain + '''.*
     ''',re.IGNORECASE | re.VERBOSE)
    
    result=Regex.findall(str1)
    print "result " + str(result)
    if result:
        for res in result:
            print "ip found " + res[0] + " " + res[1]  + " " + res[2]
            listtmp=[]
            listtmp=[res[0],res[1],res[2]]
            intlist.append(listtmp)        
    return intlist

        
def ReadFromFile(Filename):
    readfile=open(Filename,'r')
    result=readfile.read()
    return result

    
    
item=Items('mtu',finit,get_prod_mtu,get_exist_mtu,finit)
print "item is " +  str(item)
#print "item is the same : " + str (item.getstagingvalue() == item.getexistvalue)
#print "ixgbe value is " + item.getstagingvalue().strip()
print "system staging value is " + str(item.getprodvalue())
print "system existing value is " + str(item.getexistvalue())

