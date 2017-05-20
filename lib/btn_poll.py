import RPi.GPIO as GPIO
import time
import sys
import os
class Button():
        def __init__(self):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(19, GPIO.OUT)
                GPIO.output(19, True)
        def button(self):
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
                                                
                                                os.system('lpr -o fit-to-page /home/pi/image486.jpg')
                                                print 'running~'
                                        print 'check : ' + str(state)
                finally:
                        print 'end'

if __name__ == '__main__':
	but = Button()
	but.button()
