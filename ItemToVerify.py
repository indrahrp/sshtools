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

sshServer='bunkerx1'
sshUsername='root'
sshPassword='changeme'
stgdir='/var/tmp/stgdir/'
bckdir='/var/tmp/pkgbck'
connection = Ssh(sshServer, sshUsername, sshPassword)
    
itemlist={
    'ixgbe':['na','na','na'],
    'timezone':['GMT','na','na'],
    'lang':['C','na','na',]
    }

#def gethostinfo('hostname'):
#    for host in itemlist:
        
print "itemlist " + str(itemlist['ixgbe'][1])
        
def get_stage_ixgbefunc():
    
    print " checking stage ixgbe.conf"
    command="cat " +  stgdir + "ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'|sed 's/default_mtu *=//'| sed 's/ *//'"
    return connection.run_Cmd(command)


def get_exist_ixgbefunc():
    
    print "checking existing ixgbe.conf "
    command="cat /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'|sed 's/default_mtu *=//'| sed 's/ *//'"
    return connection.run_Cmd(command)
     
item=Items('ixgbe',get_stage_ixgbefunc,finit,get_exist_ixgbefunc,finit)
#print "item is " +  str(item)
###print "ixgbe value is " + item.getstagingvalue().strip()
#print "ixgbe staging value is " + item.getstagingvalue()
#print "ixgbe existing value is " + item.getexistvalue()
print "ixgbe is the same as previous : " + str (item.getstagingvalue() == item.getexistvalue())




def get_stage_system():
    print " check stage system"
    command="cat " +  stgdir + "system|grep -v ^#|sort|grep -v ^$|cksum"
    return connection.run_Cmd(command)

def get_exist_system():
    print " check existing system"
    command="cat /etc/system|grep -v ^#|sort|grep -v ^$|cksum"
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
    #print "entry " + entry
    #return entry
    mtulist=find_mtu(entry,'bunkerx1','tdn.pln.ilx.com')
    print "mtulist " + str(mtulist)
    return mtulist

def verify_mtu():
    mtuprod=item.getprodvalue()
    mtuexisting=item.getexistvalue()
    intnotmatch=[]
    for idx,value in mtuexisting.items():
        if mtuexisting[idx][1] != mtuprod[idx][1]:
            intnotmatch.append(idx)
            print " network mtu is not matched" + idx 
    return intnotmatch

def find_mtu(str1,svrname,domain):
    intdict={}    
    Regex = re.compile(r'''
    (net\d+|ixgbe\d+|igb\d+|e1000g\d+)\s+(\d+)\s+''' + svrname + '''\.(\w+)\.''' + domain + '''.*
     ''',re.IGNORECASE | re.VERBOSE)
    
    result=Regex.findall(str1)
    print "result " + str(result)
    if result:
        for res in result:
            print "ip found " + res[0] + " " + res[1]  + " " + res[2]
            listtmp=[]
            listtmp=[res[0],res[1]]
            intdict[res[2]]=listtmp       
    return intdict

        
def ReadFromFile(Filename):
    readfile=open(Filename,'r')
    result=readfile.read()
    return result

    
    
item=Items('mtu',finit,get_prod_mtu,get_exist_mtu,verify_mtu)
print "item is " +  str(item)
#print "item is the same : " + str (item.getstagingvalue() == item.getexistvalue)
#print "ixgbe value is " + item.getstagingvalue().strip()
print "mtu prod value is " + str(item.getprodvalue())
print "mtu existing value is " + str(item.getexistvalue())
print "mtu is not matched  " + str(item.item_verify_func())






    