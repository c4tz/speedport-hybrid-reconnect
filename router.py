import atexit, hashlib, json, requests
from time import sleep

class SpeedportHybrid:

	def __init__(self, password):
		self.password = password
		self.session =	requests.Session()
		self.basePath = 'http://speedport.ip'
		self.ipAPI = 'https://api.ipify.org?format=json'
		self.login()
		atexit.register(self.logout)

	def login(self):
		url = self.basePath + '/html/login/index.html?lang=de'
		r = self.session.get(url)
		challengev = r.text.split('var challenge = "')[1].split('"')[0]

		self.encryptpwd = hashlib.sha256((challengev + ':' + self.password).encode()).hexdigest()

		url = self.basePath + '/data/Login.json?lang=de'
		params = {
			'csrf_token':'nulltoken',
			'showpw':0,
			'password':self.encryptpwd,
			'challengev': challengev
		}
		r = self.session.post(url, data = params)

	def logout(self):
		url = self.basePath + '/data/Login.json?lang=de'
		params = {
			'csrf_token':'nulltoken',
			'logout':'byby'
		}
		r = self.session.post(url, data = params)

	def getDevices(self):
		r = self.session.get(self.basePath + '/data/LAN.json')

		data = r.text.replace("\\'", "'")
		data = ''.join(data.rsplit(',', 1))
		data = json.loads(data)

		devices = []
		for item in data:
			if item['varid'] == 'addmdevice' and item['varvalue'][4]['varvalue'] == '1':
				devices.append(item['varvalue'][1]['varvalue'] + ' (' + item['varvalue'][5]['varvalue'] + ')')

		return sorted(devices)

	def reconnect(self):
		oldIP = self.session.get(self.ipAPI).json()['ip']

		url = self.basePath + '/data/Connect.json?lang=de'
		params = {
			'csrf_token':'nulltoken',
			'showpw':0,
			'password':self.encryptpwd,
			'req_connect':'offline'
		}
		r = self.session.post(url, data = params)

		r = self.session.get(self.basePath + '/html/content/overview/index.html')
		token = r.text.split('csrf_token = "')[1].split('";')[0]

		sleep(0.4)
		url = self.basePath + '/data/Modules.json?lang=de'
		params = {
			'csrf_token':token,
			'lte_reconn':'1'
		}
		r = self.session.post(url, data = params)

		url = self.basePath + '/data/Connect.json?lang=de'
		params = {
			'csrf_token':'nulltoken',
			'showpw':0,
			'password':self.encryptpwd,
			'req_connect':'online'
		}
		r = self.session.post(url, data = params)

		newIP = oldIP
		while newIP == oldIP or newIP == '':
			sleep(1)
			try:
				newIP = self.session.get(self.ipAPI).json()['ip']
			except (requests.exceptions.ConnectionError):
				print('No connection yet...')
