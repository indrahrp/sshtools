'''
Created on Mar 6, 2017

@author: UC205955
'''
import threading, paramiko,time
 
class ssh:
    shell = None
    client = None
    transport = None
 
    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
 
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()
 
    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()
 
    def openShell(self):
        self.shell = self.client.invoke_shell()
 
    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")
 
    def process(self):
        global connection
        cnt=0
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata)
                strdata.replace('\r', '')
                print unicode(strdata)
                if(strdata.endswith("# ")):
                    print"\n#> ",
 
 
sshUsername = "root"
sshPassword = "changeme"
sshServer = "192.168.56.10"
 
 
connection = ssh(sshServer, sshUsername, sshPassword)
connection.openShell()
time.sleep(3)
while True:
    command = raw_input('\n# ')
    if command.startswith(" "):
        command = command[1:]
        #print "command is " + command
    
    #print "command is " + command    
    connection.sendShell(command)
 

