'''
Created on Mar 6, 2017

@author: UC205955
'''
from paramiko import SSHClient,client
from scp import SCPClient
print "in scp client"


Username = "root"
Password = "changeme"
Server = "192.168.56.10"

ssh = SSHClient()
ssh.set_missing_host_key_policy(client.AutoAddPolicy())
ssh.connect(Server, username=Username, password=Password)
        
#ssh.load_system_host_keys()
#ssh.connect('192.168.56.10')

# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())

scp.put('test.txt', 'test3.txt')
scp.get('/var/tmp/tdir','c:/temp',recursive=True)
print "scp done"

scp.close()
