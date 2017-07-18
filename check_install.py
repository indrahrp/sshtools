



#!/usr/bin/env python

'''
Created on Mar 7, 2017

@author: uc205955
'''
from SshApi2 import *
import time,re,os,json,xml.etree.ElementTree
from scp import SCPClient
from paramiko import SSHClient,client
from sse.tdnsse import *





print 'test'
print data["check_items"]["/etc/system"]
item=Items('ixgbe',get_stage_ixgbefunc,finit,get_exist_ixgbefunc,verify_ixgbe)
print "ixgbe.conf is the same as staging : " + str (item.get_verify())
