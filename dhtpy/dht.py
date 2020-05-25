import sys
import time
import datetime as dt
import RPi.GPIO as GPIO

from .dhtdata import DHTData

DEBUG = False

class DHT :

	# Sleep time between retries [s]
	sleep = 0.5
	# Samples
	samples = 2000

	#
	# Constructor
	#
	def __init__(self, pin) :
		self.pin = pin

	#
	# Single read from DHT Sensor
	#
	def __read(self) :

		_debug("Reading from GPIO: {}".format(self.pin))
		GPIO.setmode(GPIO.BCM)

		data = []

		# Set to HIGH before retrieval
		_debug("GPIO: {} - Set output to HIGH".format(self.pin))
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.HIGH)
		time.sleep(0.025)

		# Send start signal
		_debug("GPIO: {} - Send start signal".format(self.pin))
		GPIO.output(self.pin, GPIO.LOW)
		time.sleep(0.018)
		GPIO.output(self.pin, GPIO.HIGH)

                # Set to input
		_debug("GPIO: {} - Setup to input".format(self.pin))
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

		# Retrive data
		for t in range(0,self.samples) :
			data.append(GPIO.input(self.pin))

		# Set to LOW after retrieval
		_debug("GPIO: {} - Set output to LOW".format(self.pin))
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.HIGH)

		# Cleanup GPIO
		time.sleep(0.1)
		GPIO.cleanup()

		# decode message
		return self.__decode(data)


	#
	# Decode DHT message
	#
	# Protocol derived from
	# http://www.ocfreaks.com/basics-interfacing-dht11-dht22-humidity-temperature-sensor-mcu/
	#
	def __decode(self, data):

		res= [0]*5
		bits=[]
		ix = 0

		if (len(data) == 0) or all(e == 1 for e in data) :
			raise Exception("Empty data buffer")

		try:

			if data[0] == 1 :
				ix = data.index(0, ix) ## skip to first 0

			else: # skip activation bit ~80 us
				ix = data.index(1,ix) ## skip first 0's to next 1
				ix = data.index(0,ix) ## skip first 1's to next 0

			ie = data.index(1,ix) ## Find first bit 1, count 0's before bit

			chk = (ie - ix) # First LOW before bit  ~50 us / 0 bit < 30 us / 1 bit < 70 us

			_debug("Gap between bits lenght %d" %(chk))

			while len(bits) < len(res)*8 : ##need 5 * 8 bits :
				ix = data.index(1,ix) ## index of next 1
				ie = data.index(0,ix) ## nr of 1's = ie-ix
				bits.append(ie-ix)
				ix = ie

			_debug("Read %d bits. OK" %(len(bits)))

		except:
			raise Exception("Not enough data %d / 40 bits" %(len(bits)))


		# Convert to raw bytes
		for i in range(len(res)) :
			for v in bits[i*8 : (i+1)*8] :		#process next 8 bit
				res[i] = res[i]<<1  		##shift byte one place to left
				if v >= chk: res[i] += 1  	##and add 1 if lsb is 1

		if (res[0]+res[1]+res[2]+res[3])&0xff != res[4] : ##parity error!
			raise Exception("CRC error")

		_debug("CRC check. OK")

		# Convert raw bytes into engineering
		hum  = res[0]*256 + res[1]
		temp = res[2]*256 + res[3]
		if ( temp > 0x7fff ):
			temp = 0x8000 - temp

		hum  /= 10
		temp /= 10

		return DHTData(hum, temp)

	#
	# Retry read from DHT Sensor
	#
	def read(self, retries = 5) :

		for i in range(1,retries) :
			try :
				return self.__read()
			except BaseException as e:
				_debug("Attempt number %d failed. %s" %(i,str(e)))
				time.sleep(self.sleep)
				pass # Do nothing - retry

		raise Exception("Failed {} attempts...".format(i))

#
# Debug message
#
def _debug(msg) :
	if DEBUG :
		print(msg)

#
# Test
#
if __name__ == "__main__" :

	if len(sys.argv) == 2 :

		dht = DHT(int(sys.argv[1]))

		data = dht.read()

		print("temp: {} / humidity : {}".format(data.getTempCStr(), data.getHumidityStr()))

	else:
		print("Usage: " + sys.argv[0] + " <BCM GPIO>")
