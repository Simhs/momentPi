
import time
import picamera

class Dial:
  pass

class HyperLapseCam:
	def startcapture(self, timer, turns):
		timer = float(time)
		turns = int(turns)
		with picamera.PiCamera() as c:
			# c.resolution = (2592,1944) 해상도 조절
			c.exposure_compensation=2
			for i in range(turns):
				c.capture('image'+str(i)+'.jpg')
				time.sleep(timer)
	def test(self):
		pass
	
