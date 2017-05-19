#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

class Dial():
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

        def vel(self):
                trim_pot = self.readadc(self.potentiometer_adc, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)
                if(trim_pot != 0):
                        set_vel = int(round(trim_pot*705/1023))+15
                else:
                        set_vel = 0
                return set_vel
while True:
        dial = Dial()
        velue = dial.vel()
        print int(velue/60),"Hour",  int(velue%60), "Min"
