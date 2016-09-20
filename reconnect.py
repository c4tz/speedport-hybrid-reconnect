import requests
import hashlib
from time import sleep

session = requests.Session()
basePath = 'http://192.168.1.1'
password = ''

url = basePath + '/data/Login.json?lang=de'
params = {
	'csrf_token':'nulltoken',
	'showpw':0,
	'challengev':'null'
}
r = session.post(url, data = params)
challengev = r.json()[1]['varvalue']

encryptpwd = hashlib.sha256((challengev + ':' + password).encode()).hexdigest()

url = basePath + '/data/Login.json?lang=de'
params = {
	'csrf_token':'nulltoken',
	'showpw':0,
	'password':encryptpwd
}
r = session.post(url, data = params)

r = session.get(basePath + '/data/bonding_tunnel.json')
oldIP = r.text.split("'ipv4'          :'")[1].split("',")[0]

url = basePath + '/data/Connect.json?lang=de'
params = {
	'csrf_token':'nulltoken',
	'showpw':0,
	'password':encryptpwd,
	'req_connect':'offline'
}
r = session.post(url, data = params)

r = session.get(basePath + '/html/content/overview/index.html')
token = r.text.split('csrf_token = "')[1].split('";')[0]

sleep(0.4)
url = basePath + '/data/Modules.json?lang=de'
params = {
	'csrf_token':token,
	'lte_reconn':'1'
}
r = session.post(url, data = params)

url = basePath + '/data/Connect.json?lang=de'
params = {
	'csrf_token':'nulltoken',
	'showpw':0,
	'password':encryptpwd,
	'req_connect':'online'
}
r = session.post(url, data = params)

newIP = oldIP
while newIP == oldIP or newIP == '':
	sleep(1)
	r = session.get(basePath + '/data/bonding_tunnel.json')
	newIP = r.text.split("'ipv4'          :'")[1].split("',")[0]
print(newIP)

url = basePath + '/data/Login.json?lang=de'
params = {
	'csrf_token':'nulltoken',
	'logout':'byby'
}
r = session.post(url, data = params)
