'''
Created on Mar 8, 2017

@author: uc205955
'''

import paramiko,time,os,sys


sshUsername = "root"
sshPassword = "changeme"
sshServer = "192.168.56.10"
 
#client = paramiko.client.SSHClient()
#client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
#client.connect(sshServer,username=sshUsername, password=sshPassword, look_for_keys=False)


#channel = client.invoke_shell()
#channel.send('ls\n')
#time.sleep(5)
#while channel.recv_ready():
#    print channel.recv(1024)

#channel.send('exit\n')
#if channel.exit_status_ready():
#    print channel.recv_exit_status()
    
sshServer='divotz1'
#lst=['autocisco.txt', 'billa.3.py', 'billa.1.py', 'billa.2.py', 'Book1.csv', 'checkhost.py', 'checkhost.pyc', 'collect2']


def get_fname(dirnm,svrname):
    #dirnm=os.path.dirname(sys.argv[0])    
    print dirnm
    lst=os.listdir(dirnm)
    print lst 
    if_fname=lambda fname: fname if fname.startswith(svrname) else None 
    flist=list(map(if_fname,lst))
    flname=lambda fname: fname.split('.')[1]
    fno=[ flname(fname)  for fname in flist if fname is not None]

    print fno
    fnbr=[ int(fn) for fn in fno]

    if not fnbr or fnbr==0:
        flog=svrname + '.0.out'
    else:   
        flog=svrname + '.' + str(max(fnbr) + 1) + '.out'

    print flog
    fwr=open(flog,'w+')
    return fwr
        #fwr.write('test')
        
fwtowrite=get_fname('C:\Users\uc205955\workspace\sshtools','divtoz1')
#print >> f, 'Filename:', filename 

fwtowrite.write('test')