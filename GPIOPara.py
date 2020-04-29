#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import Jetson.GPIO as GPIO
import time as time


class GPIOPara():
    def __init__(self, sign_pin, pulse_pin, enable_pin):
        self.sign_pin = 0
        self.pulse_pin = 0
        self.enable_pin = 0
        self.set_sign_pin_num(sign_pin)
        self.set_pulse_pin_num(pulse_pin)
        self.set_enable_pin_num(enable_pin)
        # set the direction
        self.set_sign_pin()
        self.set_sign_high()
        # enable default: off
        self.set_enable_pin()
        self.set_enable_low()
        # GPIO.output(self.sign_pin, GPIO.LOW)  # Low:Forward  HIGH:backward
        self.change_level_flag = True

    @staticmethod
    def gpio_set():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    # change the pulse pin level
    def change_level(self, direction, pulse_num, peroid):
        if pulse_num > 0 and peroid > 0:
            pass
        else:
            return
        if direction:
            GPIO.output(self.sign_pin, GPIO.LOW) # Low:Forward  HIGH:backward
        else:
            GPIO.output(self.sign_pin, GPIO.HIGH) # Low:Forward  HIGH:backward
        count = 0
        while count <= pulse_num-1:
            time.sleep(peroid)
            self.set_pulse_high()
            time.sleep(peroid)
            self.set_pulse_low()
            count = count + 1
        self.set_pulse_high()
        # print("1")

    #################################################
    # set the sign pin
    def set_sign_pin_num(self, sign_pin):
        self.sign_pin = sign_pin

    # set the pulse pin
    def set_pulse_pin_num(self, pulse_pin):
        self.pulse_pin = pulse_pin

    ##################################################
    # set the pulse pin relative high
    def set_sign_high(self):
        GPIO.output(self.pulse_pin, GPIO.LOW)

    # set the pulse pin relative low
    def set_sign_low(self):
        GPIO.output(self.sign_pin, GPIO.HIGH)

    # set the pulse pin relative high
    def set_pulse_high(self):
        GPIO.output(self.pulse_pin, GPIO.LOW)

    # set the pulse pin relative low
    def set_pulse_low(self):
        GPIO.output(self.pulse_pin, GPIO.HIGH)

    def set_enable_high(self):
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def set_enable_low(self):
        GPIO.output(self.enable_pin, GPIO.LOW)

##################################################
    # set the pin input
    def set_pin_input(self, pin):
        GPIO.setup(pin, GPIO.IN)

    # set the pin output
    def set_pin_output(self, pin):
        GPIO.setup(pin, GPIO.OUT)

##################################################
    # set the sign output
    def set_sign_pin(self):
        self.set_pin_output(self.sign_pin)

    # set the pulse output
    def set_pulse_pin(self):
        self.set_pin_output(self.pulse_pin)

    def set_enable_pin(self):
        self.set_pin_output(self.enable_pin)

##################################################
    # the pin works only when the pin is output; free the sign pin
    def free_sign_pin(self):
        self.set_pin_input(self.sign_pin)

    # the pin works only when the pin is output; free the pulse pin
    def free_pulse_pin(self):
        self.set_pin_input(self.pulse_pin)

    def free_enable_pin(self):
        self.set_pin_input(self.enable_pin)

"""
GpioPara.gpio_set()
motor = GpioPara()
input_string = input("pulse num:")
pulse_num = int(input_string)
motor.progress(-1, pulse_num, 0.0005)
time.sleep(2)
motor.progress(0, pulse_num, 0.0005)
time.sleep(2)
motor.progress(-1, pulse_num, 0.0005)
time.sleep(2)
motor.progress(0, pulse_num, 0.0005)
time.sleep(2)
motor.progress(-1, pulse_num, 0.0005)
time.sleep(2)
motor.progress(0, pulse_num, 0.0005)
time.sleep(2)
motor.progress(-1, pulse_num, 0.0005)
time.sleep(2)
motor.progress(0, pulse_num, 0.0005)
time.sleep(2)
motor.progress(-1, pulse_num, 0.0005)
time.sleep(2)
motor.progress(0, pulse_num, 0.0005)
"""
