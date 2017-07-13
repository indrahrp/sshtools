import os,json

pwd= os.environ['SECRET']
print "pwd is "+ pwd



with open('config.json') as json_data_file:
    data = json.load(json_data_file)
#print data



print json.dumps(data, indent=4, sort_keys=True)
serverenv="hzl_prod"
print "serverenv  " + data["other"][data["hostinfo"]["server_env"]]["server_dnscheck"]