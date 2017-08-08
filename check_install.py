#!/usr/bin/env python
'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi3 import *
import sys,time,re,os,json,xml.etree.ElementTree
from scp import SCPClient
from paramiko import SSHClient,client
#from sse.tdnsse import *
from itembios import *
from types import MethodType

connection.openConn()

listobj=[]

for tocheck in data['check_items']:
    item=Items(tocheck)
    
    print "tocheck === " + tocheck
    if data['check_items'][tocheck]["check_flag"] == 'Y':
        listobj.append(item)
        for tocheckfn in data['check_items'][tocheck]:
            if not tocheckfn.strip()  == 'check_flag':
                tocheckfn_entry=data['check_items'][tocheck][tocheckfn]
                setattr(item,tocheckfn,MethodType(getattr(sys.modules["itembios"], tocheckfn_entry),item))
 
#print "\n\n\n listobj " + str(listobj)
for obj in listobj:
    
    print "===========list obj " + str(obj)
    #print obj.__dict__['check_existing']
    print obj.__dict__
    #print obj.check_staging()
    #print obj.check_existing()
    print "Exisiting and Stage is Match : " + str(obj.verify())
print "finish"

