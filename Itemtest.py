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


def find_pkgtoadd(diffe):
    
    intdict={}    

    Regex = re.compile(r'''
    (\d+a\s+)
    ((.*\s+)*)
    .  
     ''',re.IGNORECASE | re.VERBOSE)
    
    result=Regex.findall(diffe)
    print "result " + str(result)
    pkgtoadd=[] 
    if result:
        for res in result:
            print "pkg to add found: " + res[0] + " " + res[1]  
            listofpkg=res[1].split('\n') 
            print "listof pkgs " + str(listofpkg)
            for pkg in listofpkg:
		if pkg:
            		pkgtoadd.append('/usr/pkg/sbin/pkg_add ' + pkg) 
    return pkgtoadd    

def matching_pkgs():
    print " getting pkg difference ..."
    command="/usr/pkg/sbin/pkg_info| awk '{print $1}' | sort > /tmp/pkgexisting.txt"
    connection = Ssh(sshServer, sshUsername, sshPassword)
    output,errs=connection.run_Cmd_stderr(command)
        
    command1="cat /var/tmp/stgdir/pkginfo_stage.txt|awk '{print $1}' | sort > /tmp/pkgstaging.txt"
    output1,errs1=connection.run_Cmd_stderr(command1)

    command2="diff -e /tmp/pkgexisting.txt /tmp/pkgstaging.txt > /tmp/diffe"
    output2,errs2=connection.run_Cmd_stderr(command2)
    
    command3="cat /tmp/diffe"
    output3,errs3=connection.run_Cmd_stderr(command3)
      
    pkgtoadd=find_pkgtoadd(output3)
    print "pkgtoadd list " + str(pkgtoadd) 

    print "run pkg_add command ..."
    for command in pkgtoadd:
   	commandtosend="(cd /packages/solaris-11.3.10-i386;" + command + ")"
        output,errs=connection.run_Cmd_stderr(commandtosend)

item=Items('matching_pkgs',finit,finit,finit,matching_pkgs)
#print "item is " +  str(item)
print "pkg add is executing: " + str(item.get_verify())




    
