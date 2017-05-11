import getopt,sys,os,re
#from collections import OrderedDict 
import subprocess,re,pprint,csv

backupdir='/var/tmp/pkgbck/'


def find_mtu(str1,svrname,domain):
    #print "str is " + str(str1)
    intlist=[]    
    Regex = re.compile(r'''
    #(net\d+|ixgbe\d+|igb\d+|e1000g\d+)\s+\.bunkerx1\.(\w+)\.tdn.*
    (net\d+|ixgbe\d+|igb\d+|e1000g\d+)\s+(\d+)\s+''' + svrname + '''\.(\w+)\.''' + domain + '''.*
     ''',re.IGNORECASE | re.VERBOSE)

    #Regex = re.compile(r'''
    #(ixgbe\d+|igb\d+|e1000g\d+)\s+(\d+)
    #''',re.IGNORECASE | re.VERBOSE)
    
    #(ixgbe\d+|igb\d+|e1000g\d+).*mtu\s+(\d+).*\n\s+inet\s+(\d+.\d+.\d+.\d+)\s+netmask\s+(\w{8}).*\n\s+ether\s+(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})
    #''',re.IGNORECASE | re.VERBOSE)

	#ixgbe2 9000 bunkerx1.log.tdn.pln.ilx.com bunkerx1.log.tdn.pln.ilx.com 4514586 0     10052  0     0      0
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

fname='netstatii'
fentry=ReadFromFile(fname)
print "fentry  "+ fentry
mtulist=find_mtu(fentry,'bunkerx1','tdn.pln.ilx.com')
print "mtulist " + str(mtulist)