import time
import picamera

class HyperLapseCam:

	def startcapture(self, timer, turns):
		timer = float(time)
		turns = int(turns)
		with picamera.PiCamera() as c:
#			c.resolution = (2592,1944) 해상도 조절
#			c.start_preview() preview시작
			c.exposure_compensation=2
			for i in range(turns):
				c.capture('image'+str(i)+'.jpg')
				time.sleep(timer)
				i = i + 1
#			c.stop_preview() preview 끝

if __name__ == "__main__":

