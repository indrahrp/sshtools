#!/usr/bin/env python
'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi3 import *
import sys,time,re,os,json,xml.etree.ElementTree,getopt
from scp import SCPClient
from paramiko import SSHClient,client
#from sse.tdnsse import *
#from itembios import *
import itembios
from types import MethodType
#from itembios import sshPassword




def run_job(jsonfile):
    
    with open(jsonfile) as json_data_file:
        data = json.load(json_data_file)
    
    print json.dumps(data, indent=4, sort_keys=True)
    itembios.sshServer=data["hostinfo"]["host"]
    itembios.sshUsername=data["hostinfo"]["user"]
    itembios.sshPassword=os.environ['SECRET']
    itembios.zone=data["hostinfo"]["zonetype"]
    itembios.stgdir=data["hostinfo"]["stgdir"]
    itembios.bckdir=data["hostinfo"]["bckdir"]
    itembios.platform=data["hostinfo"]["platform"]
    itembios.server_env=data["hostinfo"]["server_env"]
    itembios.env_lang=data["env"]["lang"]
    itembios.env_tz_localtime=data["env"]["tz_localtime"]
    itembios.env_tz=data["env"]["env_tz"]
    itembios.server_dnsip=itembios.datalib["other"][itembios.server_env]["server_dnsip"]
    itembios.pkgdirplatf=itembios.datalib["other"]["platform"][itembios.platform]
        
    itembios.sudouser=itembios.datalib["other"][itembios.server_env]["user_sudocheck"]
    itembios.sudouserpwd=itembios.datalib["other"][itembios.server_env]["user_pwd"]
    #itembios.env_tz=data["env"]["server_dnsip"]
    
    print "in run_job "
    #itembios.connection.openConn()
    #itembios.sshServer='192.168.56.20'
    #itembios.connection.closeConnection()
    itembios.connection=Ssh(itembios.sshServer, itembios.sshUsername,itembios.sshPassword)
    itembios.connection.openConn()
    listobj=[]

    for tocheck in data['check_items']:
        item=itembios.Items(tocheck)
    
        #print "Items retrieve from json " + str(item)
        if data['check_items'][tocheck]["check_flag"] == 'Y':
            listobj.append(item)
            for tocheckfn in data['check_items'][tocheck]:
             
                if not tocheckfn.strip()  == 'check_flag':
                    tocheckfn_entry=data['check_items'][tocheck][tocheckfn]
                    setattr(item,tocheckfn,MethodType(getattr(sys.modules["itembios"], tocheckfn_entry),item))
 
    print "Check Item To be executed:"
    for obj in listobj:
        print "-" + str(obj)
    
    #f1=open('logfile','w')
    orig_stdout = sys.stdout


    svrname=itembios.sshServer
    dirnm=os.path.dirname(sys.argv[0])    
    flog=itembios.get_fname(dirnm,svrname)
    print "check log file " + str(flog)
    sys.stdout = flog
    for obj in listobj:
    
        print "======= Executing " + str(obj) + " ======="
    #print obj.__dict__['check_existing']
        #print obj.__dict__
    #print obj.check_staging()
    #print obj.check_existing()
        print "\n\nVerifying OK => : " + str(obj.verify())+ " \n\n"
        #flog.write("\n\nVerifying OK => : " + str(obj.verify())+ " \n\n")
        print "finish"

    flog.close()
    sys.stdout=orig_stdout

def usage():
    print os.path.basename(sys.argv[0]) +  " -h for help "
    print os.path.basename(sys.argv[0]) + " -f config json file to use"
    
    
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:h")
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
                if o == "-h":
                        usage()
                        sys.exit(0)
                elif o == "-f":
                    print "option f"
                    run_job(a)
            

if __name__ == "__main__":
        main()  

