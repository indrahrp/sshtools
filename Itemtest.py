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


def find_ht(biosfile):
    
    intdict={}    

    #Regex = re.compile(r'''
    #.*(Intel_R__HT_Technology).*\n
    #.*HELP_STRING.*\n
    #.*DEFAULT_OPTION.*\n
    #.*SELECTED_OPTION>\s+(\d+).*/SELECTED_OPTION>
    #''',re.IGNORECASE | re.VERBOSE )
    print "bios file " + biosfile
    Regex = re.compile(r'''
    ((\d+,\d+a\d+,\d+)\s+)+
     ''',re.IGNORECASE | re.VERBOSE )
    
    result=Regex.findall(biosfile)
    print "result " + str(result)
    if result:
        for res in result:
            print "HT found: " + res[0] + " " + res[1]  
            if '0001' in res[1]:
                return True

def matching_pkgs():
    print " getting HT setting"
    command="biosconfig -get_bios_settings > /var/tmp/biosconfig.txt"
    connection = Ssh(sshServer, sshUsername, sshPassword)
    #time.sleep(1)
    output,errs=connection.run_Cmd_stderr(command)
    #print "bisoconfig  output" + output
    
    if 'is not supported' in errs:
        command="ubiosconfig export all > /var/tmp/biosconfig.txt"
        output,errs=connection.run_Cmd_stderr(command)
        print "ubisoconfig  output" + output
        if 'is not supported' in errs:
            print "biosconfig and ubiosconfig is not supported"
            return "Unable to Determine"
        
    fname='/var/tmp/biosconfig.txt'
    #fentry=ReadFromFile(fname)
    fentry='''
121,125a132,136
< tcptraceroute-1.4nb5
< tf-zap-1.2
< tf-zephyr-2.0.4.0.43
< tiff-4.0.3nb6
< tnftp-20141104
---
'''
    print "fentry  "+ fentry
    return find_ht(fentry)
    #htset=find_ht(fentry,'bunkerx1','tdn.pln.ilx.com')
    #print "htset  " + str(htset)
    #return htset

item=Items('htsetting',finit,finit,finit,matching_pkgs)
#print "item is " +  str(item)
print "hyperthread   is  disabled : " + str(item.get_verify())




    