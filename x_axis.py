#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from Motor import Motor
from GPIOPara import GPIOPara


class x_axis(Motor):
    def __init__(self):
        super(x_axis, self).__init__()
        self.sign_pin = 12
        self.pulse_pin = 16
        self.enable_pin = 19
        self.gpio_instance = GPIOPara(self.sign_pin, self.pulse_pin, self.enable_pin)
        self.mode = True  # true: position node, false: velocity mode
        self.position = 0  # mm
        self.velocity = 0  # mm/s
        self.gear_ratio = 1

    def open_device(self):
        self.gpio_instance.set_pulse_pin()

    def close_device(self):
        self.gpio_instance.free_pulse_pin()

    def enable_on(self):
        self.gpio_instance.set_enable_high()

    def enable_off(self):
        self.gpio_instance.set_enable_low()

    def set_mode(self, mode):
        self.mode = mode

    def set_gear_ratio(self, ratio):
        if ratio <= 0:
            return
        self.gear_ratio = ratio

    def set_position(self, position):
        self.position = position  # mm

    def position_start_move(self):
        pass

    def stop_move(self):
        pass

    def set_velocity(self, velocity):
        self.velocity = velocity  # mm/s

    def velocity_start_move(self):
        pass
