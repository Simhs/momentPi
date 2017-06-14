#-*- coding: utf-8 -*-
import time
import picamera
import RPi.GPIO as GPIO
import sys
import os
from threading import Thread
import logging

class Button:    
    def __init__(self):
        self.button_state = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        GPIO.output(19, True)
        self.button_pin = 13
        GPIO.setup(13,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(13, GPIO.RISING, callback=self.handler)
        
    def handler(self, n):
        self.button_state = 1

    def start(self):
        self.button_state = 0
        
    def close(self):
        GPIO.cleanup()
        pass
        
    def getButtonValue(self):
        return self.button_state

class Dial:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        # SPI port on the ADC to the Cobbler
        self.SPICLK = 12
        self.SPIMISO = 16
        self.SPIMOSI = 20
        self.SPICS = 21
        self.POWER = 26

        # set up the SPI interface pins
        
        GPIO.setup(self.POWER, GPIO.OUT)
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS, GPIO.OUT)
        GPIO.output(self.POWER, True)
        
        # 10k trim pot connected to adc #0
        self.potentiometer_adc = 0;
        
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        
        if ((adcnum > 7) or (adcnum < 0)):
            return -1
        GPIO.output(cspin, True)
        
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
        
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
            if (commandout & 0x80):
                GPIO.output(mosipin, True)
            else:
                GPIO.output(mosipin, False)
            commandout <<= 1
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
        
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
            GPIO.output(clockpin, True)
            GPIO.output(clockpin, False)
            adcout <<= 1
            if (GPIO.input(misopin)):
                adcout |= 0x1
        
        GPIO.output(cspin, True)
        adcout >>= 1       # first bit is 'null' so drop it
                
        return adcout

    def close(self):
        GPIO.cleanup()
        pass

    def getValue(self):
        trim_pot = self.readadc(self.potentiometer_adc, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)
        if(trim_pot != 0):
            set_vel = int(round(trim_pot*705/1023))+15
        else:
            set_vel = 0
        return set_vel



class HyperLapseCam:
	def __init__(self,totaltime):
		self.totaltime = float(totaltime)
		pass
	
	def startCapture(self, timer, turns):
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
