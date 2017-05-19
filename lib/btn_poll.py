import RPi.GPIO as GPIO
import time
import sys
import os

def button():
	GPIO.setmode(GPIO.BCM)
	state = 0
	switch = 13

	GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(24,GPIO.RISING, callback=handler)

	try:
		while True:
			if GPIO.input(switch) == 0:
				while True:
					if GPIO.input(switch) == 1:
						state = 1
						print 'change : ' + str(state)
						time.sleep(0.2)
						break

				if state == 1:
					#버튼 눌러졌을시 프린트기 인쇄
					os.system('lpr -o fit-to-page /home/pi/image486.jpg')
					print 'running~'
				print 'check : ' + str(state)
	finally:
		print 'end'

if __name__ == '__main__':
	button()
#def handler(channel):
#	time.sleep(1)
#	count = 1
#	print count

#GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.add_event_detect(24,GPIO.RISING, callback=handler)
#while True:
#	time.sleep(0.5)
#	count = 0
#	print count
