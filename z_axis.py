#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from Motor import Motor
from GPIOPara import GPIOPara
import threading
import time

class x_axis(Motor):
    def __init__(self):
        super(x_axis, self).__init__()
        self.sign_pin = 32
        self.pulse_pin = 33
        self.enable_pin = 37
        self.gpio_instance = GPIOPara(self.sign_pin, self.pulse_pin, self.enable_pin)
        
        self.home = False
        self.move_mode = 0  # 0:velocity 1:position
        # velocity mode
        self.open_flag = False
        # enable

        self.mv_enable = False

        # default:velocity
        # mode choose/default mode: speed mode
        self.mv_mode = True
        # judge whether the motor is moving
        self.is_moving = False

        # the distance for every circle
        self.dis_circle = 5  # mm
        self.pulse_res = 1000  # degree for every pulse
        self.gear_ratio = 1

        # velocity mode
        self.expectedSpeed = 0
        self.expectedSpeedFlag = 0
        self.vel_start_flag = False
        self.count = 0
        # high/low level time interval
        self.vel_mode_interval = 0

        # position mode
        self.position = 0
        self.distance_pulse = 0
        self.pos_mode_expectedSpeed = 0
        self.pos_mode_expected_flag = 0
        self.pos_start_flag = False
        self.pos_mode_interval = 0

        # actual speed mm/s
        self.actualVelocity = 0

        # count the pulse to calculate the vilocity
        self.pos_count = 0

        # if self.mv_mode:
        self.vel_move_task = threading.Thread(None, self.continuous_move)
        self.pos_move_task = threading.Thread(None, self.position_move)

    def open_device(self):
        if self.open_flag:
            print("Motor is already open!")
            return
        self.gpio_instance.set_pulse_pin()
        self.open_flag = True

    def close_device(self):
        if not self.open_flag:
            print("Motor is already closed!")
            return
        self.gpio_instance.free_pulse_pin()
        self.open_flag = False

    # set motor enable
    def enable_on(self):
        if self.mv_enable:
            # print "Warning: motor is already enable!"
            return
        self.mv_enable = True
        self.gpio_instance.set_enable_low()

    def enable_off(self):
        if not self.mv_enable:
            # print "Warning: Motor is alraedy not enable!"
            return
        self.mv_enable = False
        self.gpio_instance.set_enable_high()

    def set_expectedSpeed(self, speed):
        if self.mv_mode:
            if speed > 0:
                self.expectedSpeedFlag = 1
                self.vel_mode_interval = (self.dis_circle) / (speed * self.gear_ratio * 2.0 * self.pulse_res)
                self.gpio_instance.set_sign_high()
            elif speed < 0:
                self.expectedSpeedFlag = 2
                self.vel_mode_interval = abs((self.dis_circle) / (speed * self.gear_ratio * 2.0 * self.pulse_res))
                self.gpio_instance.set_sign_low()
            elif speed == 0:
                self.expectedSpeedFlag = 0
            self.expectedSpeed = abs(speed)
        else:
            self.expectedSpeedFlag = 0

    def continuous_move(self):
        if self.mv_mode:
            while True:
                if self.mv_enable:
                    if self.vel_start_flag:
                        # print('...')
                        self.is_moving = True
                        if self.expectedSpeedFlag == 0:
                            time.sleep(0.1)
                        if self.expectedSpeedFlag == 1:
                            self.push()
                        if self.expectedSpeedFlag == 2:
                            self.pull()
                    else:
                        break
                else:
                    time.sleep(0.05)
        self.vel_start_flag = False
        self.is_moving = False

    def push(self):
        interval = 0
        if self.expectedSpeed == 0:
            return
        else:
            interval = self.vel_mode_interval
        self.gpio_instance.set_pulse_high()
        time.sleep(interval)
        self.gpio_instance.set_pulse_low()
        time.sleep(interval)
        # self.count += 1

    def pull(self):
        interval = 0
        if self.expectedSpeed == 0:
            return
        else:
            interval = self.vel_mode_interval
        self.gpio_instance.set_pulse_high()
        time.sleep(interval)
        self.gpio_instance.set_pulse_low()
        time.sleep(interval)
        # self.count += 1

    # Position Mode    #############################1
    def set_position(self, position):
        if not self.mv_mode:
            self.position = abs(position)
            self.distance_pulse = int((position * self.gear_ratio * self.pulse_res) / (self.dis_circle))
        else:
            self.position = 0
            self.distance_pulse = 0

    def set_pos_mode_expectedSpeed(self, speed):
        if not self.mv_mode:
            if speed > 0:
                self.pos_mode_interval = (self.dis_circle) / (speed * self.gear_ratio * 2.0 * self.pulse_res)
                self.pos_mode_expected_flag = 1
                self.gpio_instance.set_sign_high()
            elif speed < 0:
                self.pos_mode_interval = abs((self.dis_circle) / (speed * self.gear_ratio * 2.0 * self.pulse_res))
                self.pos_mode_expected_flag = 2
                self.gpio_instance.set_sign_low()
            elif speed == 0:
                self.pos_mode_expected_flag = 0
            self.pos_mode_expectedSpeed = abs(speed)
        else:
            self.pos_mode_expected_flag = 0
        #   print self.pos_mode_expectedSpeed

    def position_move(self):
        if not self.mv_mode:
            if self.pos_mode_expected_flag == 1:
                self.position_push()
            elif self.pos_mode_expected_flag == 2:
                self.position_pull()
            else:
                self.position = 0
                self.distance_pulse = 0
        self.pos_start_flag = False
        self.is_moving = False

    def position_push(self):
        interval = 0
        if self.position == 0 or self.pos_mode_expectedSpeed == 0:
            return
        else:
            distance = self.distance_pulse
            interval = self.pos_mode_interval
            # print(distance)
            # print(interval)
        for i in range(0, distance):
            if self.pos_start_flag:
                self.is_moving = True
                self.gpio_instance.set_pulse_high()
                time.sleep(interval)
                self.gpio_instance.set_pulse_low()
                time.sleep(interval)
            else:
                break

    def position_pull(self):
        interval = 0
        if self.position == 0 or self.pos_mode_expectedSpeed == 0:
            return
        else:
            distance = self.distance_pulse
            interval = self.pos_mode_interval
        for i in range(0, distance):
            if self.pos_start_flag:
                self.is_moving = True
                self.gpio_instance.set_pulse_high()
                time.sleep(interval)
                self.gpio_instance.set_pulse_low()
                time.sleep(interval)
            else:
                break

    def set_mode(self, mode):
        self.mv_mode = False if mode == 0 else True


    def set_gear_ratio(self, ratio):
        if ratio <= 0:
            return
        self.gear_ratio = ratio

    def start_move(self):
        if self.is_moving:
            return
        if self.mv_mode:
            self.vel_start_flag = True
            time.sleep(0.01)
            self.vel_move_task.start()
        else:
            self.pos_start_flag = True
            time.sleep(0.01)
            self.pos_move_task.start()

    def stop(self):
        if self.mv_mode:
            self.vel_start_flag = False
            self.is_moving = False
            time.sleep(0.01)
            self.vel_move_task = threading.Thread(None, self.continuous_move)
        else:
            self.pos_start_flag = False
            self.is_moving = False
            time.sleep(0.01)
            self.pos_move_task = threading.Thread(None, self.position_move)

    def is_moving_flag(self):
        if self.is_moving:
            return True
        else:
            return False

    def go_home(self):
        pass


import time
GPIOPara.gpio_set()
x_axis_motor = x_axis()
x_axis_motor.open_device()
x_axis_motor.enable_on()    
x_axis_motor.set_mode(0)
x_axis_motor.set_position(4)
x_axis_motor.set_pos_mode_expectedSpeed(1)
print(x_axis_motor.distance_pulse)
x_axis_motor.start_move()
while True:
    if x_axis_motor.is_moving_flag():
        time.sleep(0.05)
    else:
        break
x_axis_motor.stop()
