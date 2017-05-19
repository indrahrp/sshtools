'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time,re
from __builtin__ import True

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


def find_ht(biosfile,biosconfig=True):
    
    intdict={}    
    if biosconfig:
        Regex = re.compile(r'''
        .*(Intel_R__HT_Technology).*\n
        .*HELP_STRING.*\n
        .*DEFAULT_OPTION.*\n
        .*SELECTED_OPTION>\s+(\d+).*/SELECTED_OPTION>
        ''',re.IGNORECASE | re.VERBOSE )
    
    else:
        Regex = re.compile(r'''
        <Hyper-threading>(\w+)</Hyper-threading>
        ''',re.IGNORECASE | re.VERBOSE )
    
    result=Regex.findall(biosfile)
    print "result " + str(result)
    if result:
        if biosconfig:
            print "HT found from biosconfig : " + str(result[0](0)) + " " + str(result[1](1))  
            if '0001' in result[1]:
                return True
            else:
                return False
        else:
            print "HT found from ubiosconfig : " + result[0]
            if 'Disabled' in result[0]:
                return True
            else:
                 return False
         

def verify_ht():
    bios=True
    print " getting HT setting"
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
    return find_ht(output,bios)
    
item=Items('htsetting',finit,finit,finit,verify_ht)
print "hyperthread   is  disabled : " + str(item.get_verify())


