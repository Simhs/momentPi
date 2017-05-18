
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
				
	#촬영시간 입력하면 30초 영상분량을 찍어주는 메소드
	def test(self):
		timer = self.totaltime*3600/750
		with picamera.PiCamera() as c:
			c.resolution = (1920, 1080)
			for i in range(750):
				c.capture('image'+str(i)+'.jpg')
				time.sleep(timer)
				
			
	
