import serial

class MicronixSMA400(object):
	port = "COM1"
	__serialPort = None
	def __init__(self, port="COM1", autoOpen= True):
		assert(port!="")
		self.port = port
		if port!="" and autoOpen:
			self.open()

	def __del__(self):
		if self.__serialPort!=None:
			self.__serialPort.close()

	def open(self):
		if self.__serialPort!=None:
			try:
				self.__serialPort.close()
			except:
				pass
			del self.__serialPort
		self.__serialPort = serial.Serial()
		self.__serialPort.port = self.port
		self.__serialPort.baudrate=9600
		self.__serialPort.bytesize=serial.EIGHTBITS
		self.__serialPort.parity=serial.PARITY_NONE
		self.__serialPort.stopbits=serial.STOPBITS_ONE
		self.__serialPort.close()
		self.__serialPort.close()
		self.__serialPort.open()
		self.sendCommand('REFDBM')

	def sendCommand(self,command):
		assert( self.__serialPort!=None )
		self.__serialPort.write(command + '\x0D\x0A')
		result = ""
		while result.find('\x0A')==-1:
			result += self.__serialPort.read( self.__serialPort.inWaiting() )
		return result.strip()

	def hold(self):
		return self.sendCommand('HOLD')

	def run(self):
		return self.sendCommand('RUN')

	def freqsetmk(self):
		return self.sendCommand('FREQSETMK')

	def measres(self):
		return self.sendCommand('MEASRES')

	@property
	def freq(self):
		return self.sendCommand('FREQ?')

	@freq.setter
	def freq(self, value):
		self.sendCommand('FREQ'+value)

	@property
	def span(self):
		return self.sendCommand("SPAN?")

	@span.setter
	def span(self,value):
		assert( value in ('ZERO', '200K', '500K', '1M', '2M', '5M', '20M', '50M', '100M', '200M', '500M', '1G', '2G', 'FULL') )
		self.sendCommand('SPAN'+value)

	@property
	def ref(self):
		return self.sendCommand('REF?')

	@ref.setter
	def ref(self,value):
		assert( value>=-60 and value<=10 )
		self.sendCommand('REF'+str(value))

	@property
	def rbw(self):
		return self.sendCommand('RBW?')

	@rbw.setter
	def rbw(self,value):
		assert( value in ('3K', '10K', '30K', '100K', '1M', '3M', 'AUTO', 'ALL') )
		self.sendCommand('RBW'+str(value))

	@property
	def vbw(self):
		return self.sendCommand("VBW?")

	@vbw.setter
	def vbw(self, value):
		value = str(value)
		assert( value in ( '100', '300', '1K', '3K', '10K', '30K', '100K', '300K', '1M', 'AUTO', 'ALL' ) )
		self.sendCommand('VBW'+value)

	@property
	def meas(self):
		return self.sendCommand('MEAS')

	@meas.setter
	def meas(self, value):
		value = str(value)
		assert( value in ( 'CP', 'ACP', 'OBW', 'EF', 'MF', 'FC', 'OFF' ) )
		self.sendCommand('MEASOFF')
		self.sendCommand('MEAS'+value)