#
# Data container
#
class DHTData :

	#
	# Constructor
	#
        def __init__(self, h, t) :
                self.h = h
                self.t = t

        def getHumidity(self) :
                return self.h

        def getHumidityStr(self) :
                return "{} %".format(self.getHumidity())

        def getTempC(self) :
                return self.t

        def getTempCStr(self) :
                return "{} ºC".format(self.getTempC())

        def getTempFarenheit(self) :
                return self.t * 9 / 5 + 32

        def getTempFStr(self) :
                return "{} ºF".format(self.getTempF())
