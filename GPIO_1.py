#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time as time

class GpioPara():
    def __init__(self):
        self.pulse_in = 19
        GPIO.setup(self.pulse_in, GPIO.OUT)
        
    @staticmethod
    def gpio_set():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def set_value_high(self):
        GPIO.output(self.pulse_in, GPIO.HIGH)
        #print("value:", value)

    def gpio_clean(self):
        GPIO.cleanup()

GpioPara.gpio_set()
motor = GpioPara()
motor.set_value_high()

