#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time as time

class GpioPara():
    def __init__(self):
        self.pulse_pin = 7
        GPIO.setup(self.pulse_pin, GPIO.OUT)
        
    @staticmethod
    def gpio_set():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)


    def progress(self, direction, pulse_num, peroid):
        if direction:
            GPIO.output(self.sign_pin, GPIO.LOW) # Low:Forward  HIGH:backward
        else:
            GPIO.output(self.sign_pin, GPIO.HIGH) # Low:Forward  HIGH:backward
        count = 0
        while (count <= pulse_num-1):
            time.sleep(peroid)
            self.set_high()
            time.sleep(peroid)
            self.set_low()
            count = count + 1
        self.set_high()
        #print("1")

    def set_high(self):
        GPIO.output(self.pulse_pin, GPIO.LOW)

    def set_low(self):
        GPIO.output(self.pulse_pin, GPIO.HIGH)

GpioPara.gpio_set()
motor = GpioPara()
#time.sleep(5)
#motor.set_high()
#time.sleep(5)
motor.set_low()
