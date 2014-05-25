import serial
import time
import re

MSA438 = 0
MSA458 = 1
MSA438E = 2


class MicronixMSA400(object):
	"""Driver for MicronixMSA400"""
	port = "COM1"
	devModel = MSA438
	__serialPort = None
	def __init__(self, port="COM1", autoOpen= True):
		assert(port!="")
		self.port = port
		if port!="" and autoOpen:
			self.open()

	def __del__(self):
		if self.__serialPort is not None:
			self.__serialPort.close()

	def open(self):
		if self.__serialPort is not None:
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

	def close(self):
		if self.__serialPort is not None:
			self.__serialPort.close()

	def sendCommand(self,command, endTurple = True, sleepTime = 3):
		assert( self.__serialPort is not None )
		self.__serialPort.write(command + '\x0D\x0A')
		result = ""
		if endTurple:
			while result.find('\x0D\x0A')==-1:
				result += self.__serialPort.read( self.__serialPort.inWaiting() )
		else:
			last = time.time()
			rd = 0
			while ( time.time()-last )<2:
				rd = self.__serialPort.inWaiting()
				if rd>0:
					last = time.time()
					result += self.__serialPort.read( rd )
					self.__serialPort.flush()
		return result.strip()

	def hold(self):
		return self.sendCommand('HOLD')

	def run(self):
		return self.sendCommand('RUN')

	def freqsetmk(self):
		return self.sendCommand('FREQSETMK')

	def measres(self):
		return self.sendCommand('MEASRES',False,10)
		
	def autotune(self):
		return self.sendCommand('AUTO')

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
		value = value.upper()
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
		value = value.upper()
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
		
	@property
	def cpmode(self):
		return self.sendCommand('CPMODE?')
	
	@cpmode.setter
	def cpmode(self, value):
		value = str(value)
		assert( value in ('TOTAL', 'BAND') )
		self.sendCommand('CPMODE'+value)
		
	@property
	def cpcntr(self):
		return self.sendCommand('CPCNTR?')
	
	@cpcntr.setter
	def cpcntr(self,value):
		value = str(value)
		self.sendCommand( 'CPCNTR' + value )
		
	@property
	def cpwidth(self):
		return self.sendCommand( 'CPWIDTH?' )
		
	@cpwidth.setter
	def cpwidth(self,value):
		self.sendCommand('CPWIDTH' + str(value))
		
	@property
	def acpmode(self):
		return self.sendCommand('ACPMODE?')
		
	@acpmode.setter
	def acpmode(self, value):
		value = str(value).upper()
		assert( value in ('TOTAL', 'BAND', 'PEAK') )
		self.sendCommand( 'ACPMODE'+value )
		
	@property
	def calc(self):
		return self.sendCommand('CALC?')
	@calc.setter
	def calc(self, value):
		value = str(value).upper()
		assert( value in ( 'OFF','MAX','MIN','AVE','OVR' ) )
		self.sendCommand('CALC'+value)
		
	@property
	def maxno(self):
		return self.sendCommand('MAXNO?')
		
	@maxno.setter
	def maxno(self, value):
		assert( int(value) in ( 2,4,8,16,32,64,128,256,512,1024,0 ) )
		self.sendCommand( 'MAXNO'+str(value) )
		
	@property
	def minno(self):
		return self.sendCommand( 'MINNO?' )
		
	@minno.setter
	def minno(self, value):
		assert( int(value) in ( 2,4,8,16,32,64,128,256,512,1024,0 ) )
		self.sendCommand( 'MINNO'+str(value) )
		
	@property
	def aveno(self):
		return self.sendCommand( 'AVENO?' )
		
	@aveno.setter
	def aveno(self, value):
		assert( int(value) in ( 2,4,8,16,32,64,128,256,512,1024,0 ) )
		self.sendCommand( 'AVENO'+str(value) )
		
	@property
	def ovrno(self):
		return self.sendCommand('OVRNO?')
		
	@ovrno.setter
	def ovrno(self,value):
		assert( int(value) in ( 2,4,8,16,32,64,128,256,512,1024,0 ) )
		self.sendCommand( 'OVRNO'+str(value) )
		
	@property
	def scale(self):
		return self.sendCommand('SCALE?')
		
	@scale.setter
	def scale(self,value):
		assert( int(value) in (2,5,10) )
		self.sendCommand( 'SCALE'+ str(value) )
		
	@property
	def sweep(self):
		return self.sendCommand('SWEEP?')
		
	@sweep.setter
	def sweep(self,value):
		value = str(value).upper()
		value = value.replace('.',',')
		assert( str(value) in ( '10M' , '30M' , '0,1S' , '0,3S' , '1S' , '3S' , '10S' , '30S' , 'AUTO' , 'ALL' ) )
		self.sendCommand( 'SWEEP'+value )
		
		
	@property
	def det(self):
		return self.sendCommand('DET?')
		
	@det.setter
	def det(self, value):
		value = str(value).upper().strip()
		assert( value in ('POS' , 'NEG' , 'SMP') )
		self.sendCommand( 'DET'+value )
		
	
	@property
	def trg(self):
		return self.sendCommand('TRG?')
		
	@trg.setter
	def trg(self, value):
		value = str(value).upper().strip()
		assert( value in ('INT','EXT') )
		self.sendCommand('TRG'+value)
		
	def mkrres(self):
		return self.sendCommand('MKRRES')

	@property
	def mkr(self):
		return self.sendCommand('MKR?')

	@mkr.setter
	def mkr(self, value):
		value = str(value).upper().strip()
		assert( value in ('NORM','DELTA') )
		self.sendCommand('MKR'+value)

	@property
	def normkr(self):
		return self.sendCommand( 'NORMMKR?' )

	@normkr.setter
	def normmkr(self, value):
		assert( int(value)>=0 and int(value)<=500 )
		self.sendCommand( 'NORMKR' + str(value) )

	@property
	def peak(self):
		return self.sendCommand('PEAK?')

	@peak.setter
	def peak(self, value):
		value = str(value).upper().strip()
		assert( value in ( 'NORM', 'PEAK' ) )
		self.sendCommand( 'PEAK'+value )

	@property
	def pksearch(self):
		return self.sendCommand('PKSEARCH?')

	@pksearch.setter
	def pksearch(self, value):
		assert( value in ( '01' , '02' , '03' , '04' , '05' , '06' , '07' , '08' , '09', '10' , '11') )
		self.sendCommand( "PKSEARCH" + str(value) )


	@staticmethod
	def freq2HZ(data):
		scale = re.findall('[MKG]',data)[0]
		o = re.findall('[\d+\.]+',data)[0]
		o =  float(o)
		return {
			'G': int(o * 1000000000),
			'M': return int(o * 1000000),
			'K': return int(o*1000)
		}.get(scale)


	def srsf(self):
		data = self.sendCommand( 'SRSF' , False)
		parts = re.findall('CF\s(\S+)\s+SP\s(\S+)\s+RF\s(\S+)\s+ST\s(\S+)\s(\S+)\s+RB\s(\S+)\s+VB\s(\S+)\s+SC\s(\S+)',data)
		spects = re.findall('(-\d+\.\d+)',data)

