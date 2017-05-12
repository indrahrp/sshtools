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
localstgdir='/var/tmp/stgdir/'


itemlist={
    'ixgbe':['sol1','na','local','']
    }

#def gethostinfo('hostname'):
#    for host in itemlist:
        
print "itemlist " + str(itemlist['ixgbe'][1])
 

def ReadFromFile(Filename):
    readfile=open(Filename,'r')
    result=readfile.read()
    return result

def verify_ntp():
    
    print " verifying ntp"
    command="xntpdc -c peers"
    connection = Ssh(sshServer, sshUsername, sshPassword)
    time.sleep(3)
    output,errs=connection.run_Cmd_stderr(command)
    print "ntp output" + output
    #return entry
    #return output ==  None
    if 'Connection refused' in errs:
        return False
    else:   
        return True

item=Items('ntp',finit,finit,finit,verify_ntp)
print "item is " +  str(item)
print "ntp  is  working : " + str(item.get_verify())


def verify_ht():
    print " getting HT setting"
    fname='biossettings.xml'
    fentry=ReadFromFile(fname)
    print "fentry  "+ fentry
    #htset=find_ht(fentry,'bunkerx1','tdn.pln.ilx.com')
    #print "htset  " + str(htset)
    #return htset

item=Items('htsetting',finit,finit,finit,verify_ht)
print "item is " +  str(item)
print "hyperthread   is  disabled : " + str(item.get_verify())


def verify_sudo():
    print "verifying sudo \n login using ravind account ... "

    command="s" +  localstgdir + "system|grep -v ^#|sort|grep -v ^$|cksum"
    sshUsername='test1'
    sshPassword='changeme'    
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #connection.openShell()
    time.sleep(3)
        #return connection.sendShell(command)
    connection.openShellsudo()
    output=connection.sendShellsudo('sudo -l')
    print "output send shell " + output
    if "assword" in output:
        output=connection.sendShellsudo(sshPassword)
    print "output after sending password " + output
    if 'may run the following commands' in output:
        return True

item=Items('sudo',finit,finit,finit,verify_sudo)
print "item is " +  str(item)
print "sudo is working : " + str(item.get_verify())




    