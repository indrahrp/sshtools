'''
Created on Mar 8, 2017

@author: uc205955
'''

import paramiko,time


sshUsername = "root"
sshPassword = "changeme"
sshServer = "192.168.56.10"
 
client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
client.connect(sshServer,username=sshUsername, password=sshPassword, look_for_keys=False)


channel = client.invoke_shell()
channel.send('ls\n')
time.sleep(5)
while channel.recv_ready():
    print channel.recv(1024)

channel.send('exit\n')
if channel.exit_status_ready():
    print channel.recv_exit_status()