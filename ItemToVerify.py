#!/usr/bin/env python
'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time,re,os

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


sshServer='192.168.56.20'
sshUsername='root'


sshPassword=os.environ['SECRET']
print "pwd is "+ sshPassword
stgdir='/var/tmp/stgdir/'
bckdir='/var/tmp/pkgbck'

itemlist={
    #'ixgbe':['na','na','na'],
    'env_tz':['GMT','na','na'],
    'tz_localtime':['GMT','na','na'],
    'lang':['C','na','na',]
    }





connection = Ssh(sshServer, sshUsername, sshPassword)


    

def ReadFromFile(Filename):
    readfile=open(Filename,'r')
    result=readfile.read()
    return result

    
        
def get_stage_ixgbefunc():
    
    print "checking stage ixgbe.conf"
    command= "cat /var/tmp/stgdir/ixgbe.conf|sort|grep -v ^# | cksum| awk '{print $2}'"
    #command="cat " +  stgdir + "ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'|sed 's/default_mtu *=//'| sed 's/ *//'"
    return connection.run_Cmd(command)


def get_exist_ixgbefunc():
    
    print "checking existing ixgbe.conf "
    command= "cat /kernel/drv/ixgbe.conf|sort|grep -v ^#| cksum | awk '{print $2}'"
    
    #command="cat /kernel/drv/ixgbe.conf|grep -i mtu|grep -iv ^#|grep 'default_mtu'|sed 's/default_mtu *=//'| sed 's/ *//'"
    return connection.run_Cmd(command)
     
item=Items('ixgbe',get_stage_ixgbefunc,finit,get_exist_ixgbefunc,finit)
print "ixgbe.conf is the same as staging : " + str (item.getstagingvalue() == item.getexistvalue())



def get_stage_system():
    print "check stage /etc/system"
    command="cat " +  stgdir + "system|grep -v ^*|sort|grep -v ^$|cksum|awk '{print $2}'"
    return connection.run_Cmd(command)

def get_exist_system():
    print "check existing /etcsystem"
    command="cat /etc/system|grep -v ^*|sort|grep -v ^$|cksum | awk '{print $2}'"
    return connection.run_Cmd(command)

def verify_system():
    if item.getexistvalue().strip() == '0' or item.getstagingvalue().strip() == '0':
        print "cksum of /etc/system file is 0 check manually "
        return False
    if item.getexistvalue().strip() == item.getstagingvalue().strip():
        return True
    
item=Items('system',get_stage_system,finit,get_exist_system,verify_system)
print "existing /etc/system is the same as staging : " +  str (item.get_verify())


def get_stage_ndd():
    print "check stage /etc/rc2.d/S68ndd "
    command="cat " +  stgdir + "S68ndd|egrep -vi '(^#|^$)'|sort | awk '{print $5}' |cksum|awk '{print $2}'"
    #connection.run_Cmd(command)
    return connection.run_Cmd(command).strip()

def get_exist_ndd():
    print "checking  existing /etc/rc2.d/S68ndd and what it is on the memory "
    command="cat /etc/rc2.d/S68ndd |sort|grep -v '^#'|grep -v '^$'|awk '{print $5}'|cksum|awk '{print $2}'"
    command1="(cat /etc/rc2.d/S68ndd|egrep -vi '(^#|^$)'|sort| sed 's/-set/-get/'|sed 's/[0-9]*//g' > /tmp/s && bash /tmp/s|cksum | awk '{print $2}')"
    if connection.run_Cmd(command).strip() == connection.run_Cmd(command1).strip():
        return connection.run_Cmd(command).strip() 
    else:
        print "Existing /etc/rc2.d/S68ndd needs to be executed"
        return 0

item=Items('S68ndd',get_stage_ndd,finit,get_exist_ndd,finit)
print "existing /etc/rc2.d/S68ndd is the same as staging : " +  str (item.getstagingvalue() == item.getexistvalue())





def get_prod_mtu():
    print "getting previous prod mtu"
    command='cat /var/tmp/pkgbck/netstatii'
    fentry=connection.run_Cmd(command)
    mtulist=find_mtu(fentry,sshServer,'tdn.pln.ilx.com')
    print "mtulist " + str(mtulist)
    return mtulist

def get_exist_mtu():
    print "getting current server mtu"
    command="netstat -i | grep -i " + sshServer
    time.sleep(3)
    entry=connection.run_Cmd(command)
    mtulist=find_mtu(entry,sshServer,'tdn.pln.ilx.com')
    print "mtulist " + str(mtulist)
    return mtulist

def verify_mtu():
    mtuprod=item.getprodvalue()
    mtuexisting=item.getexistvalue()
    intnotmatch=[]
    for idx,value in mtuexisting.items():
        if mtuexisting[idx][1] != mtuprod[idx][1]:
            intnotmatch.append(idx)
            #print " network mtu is not matched" + idx 
    return intnotmatch

def find_mtu(str1,svrname,domain):
    intdict={}    
    Regex = re.compile(r'''
    (nge\d+|nxge\d+|net\d+|ixgbe\d+|igb\d+|e1000g\d+)\s+(\d+)\s+''' + svrname + '''\.(\w+)\.''' + domain + '''.*
     ''',re.IGNORECASE | re.VERBOSE)
    
    result=Regex.findall(str1)
    #print "result " + str(result)
    if result:
        for res in result:
            #print "ip found " + res[0] + " " + res[1]  + " " + res[2]
            listtmp=[]
            listtmp=[res[0],res[1]]
            intdict[res[2]]=listtmp       
    return intdict


    
item=Items('mtu',finit,get_prod_mtu,get_exist_mtu,verify_mtu)
print "List of interface which mtu are not matched with previous : " + str(item.item_verify_func())


def verify_lang():
    command="svccfg -s svc:/system/environment:init listprop environment/LANG|awk '{print $3}'"
    entry=connection.run_Cmd(command)
    return (entry.strip() == itemlist['lang'][0])
    

item=Items('lang',finit,finit,finit,verify_lang)
print "Lang is matched with Staging : " + str(item.item_verify_func())

def verify_tz_localtime():
    command="svccfg -s svc:/system/timezone:default listprop timezone/localtime|awk '{print $3}'"
    entry=connection.run_Cmd(command)
    print "entry " + entry
    return (entry.strip() == itemlist['tz_localtime'][0])

item=Items('Timezone/localtime',finit,finit,finit,verify_tz_localtime)
print "Timezone/localtime  is matched with staging :  " + str(item.item_verify_func())


def verify_env_tz():
    #print "env_tz "+ itemlist['env_tz'][0]
    command1="svccfg -s system/environment:init listprop environment/TZ| awk '{print $3}'"
    entry1=connection.run_Cmd(command1)
    command2="cat /etc/TIMEZONE |grep LANG|awk -F= '{print $2}'"
    entry2=connection.run_Cmd(command2)
    command3="cat /etc/TIMEZONE |grep TZ|awk -F= '{print $2}'"
    entry3=connection.run_Cmd(command3)
    print "entry " + entry1
    return (entry1.strip() == itemlist['env_tz'][0] and entry2.strip() == itemlist['lang'][0] and entry3.strip() == itemlist['env_tz'][0] )

item=Items('environment/timezone',finit,finit,finit,verify_env_tz)

print "Environment/Timezone is matched with staging :  " + str(item.item_verify_func())

def verify_bps():
    print "veryfying bps.sh "
    command="(rm /var/tmp/bps.log;/bps.sh)"
    output,errs=connection.run_Cmd_stderr(command)
    command="cat /var/tmp/bps.log"
    entry=connection.run_Cmd(command)
    return ('Operation SUCCESS' in entry.strip())

item=Items('verify_bps',finit,finit,finit,verify_bps)

print "bps.sh is working :  " + str(item.item_verify_func())



def verify_profile():
    #print "env_tz "+ itemlist['env_tz'][0]
    command1="cksum /etc/profile | awk '{print $2}'"
    entry1=connection.run_Cmd(command1)
    print "entry " + entry1
    command2="cksum /var/tmp/pkgbck/profile | awk '{print $2}'" 
    entry2=connection.run_Cmd(command2)
    command3="(cd /etc/profile.d && ls | cksum | awk '{print $2}')"
    entry3=connection.run_Cmd(command3)
    print "entry " + entry3
    command4="(cd /var/tmp/pkgbck/profile.d && ls|cksum |awk '{print $2}')" 
    entry4=connection.run_Cmd(command4)
    print "entry " + entry4
    
    return (entry1.strip() == entry2.strip() and entry3.strip() == entry4.strip())

item=Items('/etc/profile',finit,finit,finit,verify_profile)

print "/etc/profile and /etc/profile.d/* matched the previous OS :  " + str(item.item_verify_func())

def verify_prodeng():
    command1="cksum /etc/prodeng.conf | awk '{print $2}'"
    entry1=connection.run_Cmd(command1)
    print "entry " + entry1
    command2="cksum /var/tmp/pkgbck/prodeng.conf| awk '{print $2}'"
    entry2=connection.run_Cmd(command2)
    
    return (entry1.strip() == entry2.strip())

item=Items('/etc/prodeng.conf',finit,finit,finit,verify_prodeng)

print "/etc/prodeng.conf matched the previous OS :  " + str(item.item_verify_func())


def verify_zephyr():
    #print "env_tz "+ itemlist['env_tz'][0]
    command1="cksum /etc/zephyr.servers | awk '{print $2}'"
    entry1=connection.run_Cmd(command1)
    print "entry " + entry1
    command2="cksum /var/tmp/pkgbck/zephyr.servers | awk '{print $2}'" 
    entry2=connection.run_Cmd(command2)
    return (entry1.strip() == entry2.strip())

item=Items('/etc/zephyr.servers',finit,finit,finit,verify_zephyr)

print "/etc/zephyr.servers matched the previous OS :  " + str(item.item_verify_func())
    


def verify_email():
    #print "env_tz "+ itemlist['env_tz'][0]
    connection.openShell()
    output=connection.cmdtoShell('mailx indra.harahap@thomsonreuters.com')
    print "output send shell " + output
    if "ubject" in output:
        output=connection.cmdtoShell('email test')
        print "output after putting in subject  " + output
    if "test" in output:
        output=connection.cmdtoShell('.')
        print "output after putting 'period' " + output
    if 'EOT' in output:
        return True
    else:
        return False
    
item=Items('mailx',finit,finit,finit,verify_email)

print "mailx is successfully sent (check also your inbox) :  " + str(item.item_verify_func())

def verify_etcgateways():
    command1="cksum /etc/gateways| awk '{print $2}'"
    entry1=connection.run_Cmd(command1)
    print "entry " + entry1
    command2="cksum /var/tmp/pkgbck/gateways| awk '{print $2}'"
    entry2=connection.run_Cmd(command2)
    
    return (entry1.strip() == entry2.strip())

item=Items('/etc/gateways',finit,finit,finit,verify_etcgateways)

print "/etc/gateways matched the previous OS :  " + str(item.item_verify_func())

def verify_dns():
    
    print " verifying DNS"
    #command="nslookup birdiex1.gtdl.tdn.pln.ilx.com"
    command="nslookup birdiez1"
    output,errs=connection.run_Cmd_stderr(command)
    print "dns output" + output
    if '127.0.0.1' in output and '10.186.7.5' in output:
        return True
    else:   
        return False


item=Items('DNS',finit,finit,finit,verify_dns)
print "DNS cache is  working : " + str(item.get_verify())

def verify_var_tmp():
    
    print " verifying permission /var/tmp"
    command="ls -ltrd /var/tmp/"
    output,errs=connection.run_Cmd_stderr(command)
    print "ls -ltrd /var/tmp/ " + output
    if 'drwxrwxrwt' in output:
        return True
    else:   
        return False


item=Items('var_tmp',finit,finit,finit,verify_var_tmp)
print "/var/tmp/ permission is correct: " + str(item.get_verify())

def verify_ftp():
    
    print " verifying ftp enabled"
    command="svcs -a|grep network/ftp"
    output,errs=connection.run_Cmd_stderr(command)
    print "ftp output : " + output
    if 'online' in output and 'disabled' not in output:
        return True
    else:   
        return False


item=Items('FTP',finit,finit,finit,verify_ftp)
print "FTP service   is  enabled: " + str(item.get_verify())


def verify_ntp():
    
    print " verifying ntp"
    command="xntpdc -c peers"
    output,errs=connection.run_Cmd_stderr(command)
    print "ntp output" + output
    if 'Connection refused' in errs:
        return False
    else:   
        return True

item=Items('ntp',finit,finit,finit,verify_ntp)
print "ntp  is  working : " + str(item.get_verify())




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
            print "HT found from biosconfig : " + str(result[0][0]) + " " + str(result[0][1])  
            if '0001' in result[0][1]:
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


def verify_sudo():
    print "verifying sudo \n login using ravind account ... "
    
    sshUsername='indrah'
    sshPassword='h0gKRmqU'
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

item=Items('sudo',finit,finit,finit,verify_sudo)
print "sudo is working : " + str(item.get_verify())

def verify_sysadmin():
    print "verifying /etc/sysadmin/host and services soft links :"
    Flag=True
    command="ls -l /etc/hosts"
    output=connection.run_Cmd(command)
    m = re.match(r"(.*/etc/hosts -> .*/inet/hosts)",output)
    if not m:
        print "soft link /etc/hosts -> /etc/inet/hosts is not created correctly"
        Flag=False
        
    command="ls -l /etc/services"
    output=connection.run_Cmd(command)
    m = re.match(r"(.*/etc/services -> .*/inet/services)",output)
    if not m:
        print "soft link /etc/services -> /etc/inet/services is not created correctly"
        Flag=False
  
    command="ls -l /etc/inet/hosts"
    output=connection.run_Cmd(command)
    m = re.match(r"(.*/etc/inet/hosts -> .*/sysadmin/hosts)",output)
    if not m:
        print "soft link /etc/inet/hosts -> /etc/sysadmin/hosts is not created correctly"
        Flag=False
    
    command="ls -l /etc/inet/services"
    output=connection.run_Cmd(command)
    m = re.match(r"(.*/etc/inet/services -> .*/sysadmin/services)",output)
    if not m:
        print "soft link /etc/inet/services -> /etc/sysadmin/services  is  not created"
        Flag=False  
    
    command="cat /etc/hosts"
    output=connection.run_Cmd(command) 
    if 'can not open'  in output:
        print "cat /etc/hosts can not open , soft link is messed up"
        Flag=False
        
    command="cat /etc/services"
    output=connection.run_Cmd(command)
    if 'can not open'   in output:
        print "cat /etc/services  can not open , soft link is messed up"
        Flag=False
    return Flag

item=Items('/etc/sysadmin',finit,finit,finit,verify_sysadmin)
print "/etc/sysadmin softlink is correct : " + str(item.get_verify())


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
    
    print " diff -e output ..."
    command3="cat /tmp/diffe"
    output3,errs3=connection.run_Cmd_stderr(command3)
      
    pkgtoadd=find_pkgtoadd(output3)
    print "pkgtoadd list " + str(pkgtoadd) 

    print "run pkg_add command ..."
    for command in pkgtoadd:
         commandtosend="(cd /packages/solaris-11.3.10-i86pc/;" + command + ")"
         output,errs=connection.run_Cmd_stderr(commandtosend)

#item=Items('matching_pkgs',finit,finit,finit,matching_pkgs)
#print "item is " +  str(item)
#print "pkg add is executing: " + str(item.get_verify())


def verify_pkgs():
    #print "env_tz "+ itemlist['env_tz'][0]
    command1="/usr/pkg/sbin/pkg_info | awk '{print $1}'| sort > /tmp/pkgexist.txt "
    entry1=connection.run_Cmd(command1)
    print "entry " + entry1
    command2="cat /var/tmp/stgdir/pkginfo_stage.txt | awk '{print $1}'|sort > /tmp/pkgstg.txt" 
    entry2=connection.run_Cmd(command2)
    command3="diff /tmp/pkgexist.txt /tmp/pkgstg.txt"
    #return (entry1.strip() == entry2.strip())
    entry3=connection.run_Cmd(command3)
    return "check above output"

item=Items('pkg_info',finit,finit,finit,verify_pkgs)

print "pkg_info difference between  staging and existing  :  " + str(item.item_verify_func())



    
    
    

    
