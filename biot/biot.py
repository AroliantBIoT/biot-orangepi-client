from socketIO_client import SocketIO, LoggingNamespace

APP_NAME = "BIoT"


class BIoT:
	connected = False

	def __init__(self, host=False, port=False, params={}):

		self.connected = False
		self.param_call = {}
		self.param_functions = {}

		if host is False:
			print("Error : Host not Specified")

		elif port is False:
			print("Error : Port not Specified")

		else:
			print(APP_NAME + " : Trying to connect " + host + " via port " + str(port))

			self.IO = SocketIO(host, port, params=params)
			self.IO.on('connect', self.on_connect)
			self.IO.on('disconnect', self.on_disconnect)
			self.IO.on('param:change', self.param_change)

	def on_connect(self):
		self.connected = True
		print(APP_NAME + ' : Connected to Server')

	def on_disconnect(self):
		self.connected = False
		print(APP_NAME + ' : Disconnected from Server')

	def on_reconnect(self):
		print(APP_NAME + ' : Trying to Reconnect')

	def param_change(self, device):
		for device_id, params in self.param_call.items():
			for key, function in params.items():
				print(dict(device))
				if device['id'] == int(device_id) and device['param'].encode("utf-8") == key:
					self.param_functions[device_id][key](device['value'])

	def wait(self, time=None):
		if not time:
			self.IO.wait()
		else:
			self.IO.wait(time)

	def on_param_change(self, param, device_id, callback):
		self.param_call[str(device_id)][param] = callback.__name__
		self.param_functions[str(device_id)][param] = callback

		print("Callback to " + callback.__name__ + " registered on " + param + " change")

	def setState(self, id, param, value):
		message = {'id': id, 'param': param, 'value': value}
		self.IO.emit("device:set:state", message)

	def getState(self, param):
		pass
