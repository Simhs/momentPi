
import time
import picamera

class Dial:
  pass

class HyperLapseCam:
	def __init__(self,totaltime):
		self.totaltime = float(totaltime)
		pass
	
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
		timer = self.totaltime*3600/750
		with picamera.PiCamera() as c:
			c.resolution = (1920, 1080)
			for i in range(750):
				c.capture('image'+str(i)+'.jpg')
				time.sleep(timer)
				
			
	
