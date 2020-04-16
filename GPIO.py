#!/usr/bin/env python3

import Jetson.GPIO as GPIO
import time as time

class GpioPara():
    def __init__(self):
        self.sign_pin = 12
        self.pulse_pin = 16
        GPIO.setup(self.sign_pin, GPIO.OUT)
        GPIO.setup(self.pulse_pin, GPIO.OUT)
        GPIO.output(self.sign_pin, GPIO.LOW) # Low:Forward  HIGH:backward
        
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
input_string = input("pulse num:")
pulse_num = int(input_string)
motor.progress(0, pulse_num, 0.0005)
time.sleep(3)
motor.progress(1, pulse_num, 0.0005)
time.sleep(3)
motor.progress(0, pulse_num, 0.0005)
time.sleep(3)
motor.progress(1, pulse_num, 0.0005)
time.sleep(3)
motor.progress(0, pulse_num, 0.0005)
time.sleep(3)
motor.progress(1, pulse_num, 0.0005)
time.sleep(3)
motor.progress(0, pulse_num, 0.0005)
time.sleep(3)
motor.progress(1, pulse_num, 0.0005)
time.sleep(3)
motor.progress(0, pulse_num, 0.0005)
time.sleep(3)
motor.progress(1, pulse_num, 0.0005)

