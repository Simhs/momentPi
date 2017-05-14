import time
import sys
import picamera

def test(t, turns):
	t = float(t)
	turns = int(turns)
	name = 0
	with picamera.PiCamera() as c:
#		c.resolution = (2592,1944)
		c.start_preview()
		c.exposure_compensation=2
#c.exposure_mode = 'spotlight'
#	c.meter_mode = 'matrix'
#	c.image_effect = 'gpen'
		time.sleep(t)
		c.exif_tags['IFD0.Artist'] = 'Kim'
		c.exif_tags['IFD0.Copyright'] = 'Copyright Kim'
		for _ in range(turns):
			c.capture('image'+str(name)+'.jpg')
			time.sleep(t)
			name = name + 1
		c.stop_preview()

if __name__ == "__main__":
	test(sys.argv[1], sys.argv[2])
