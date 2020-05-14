#!/usr/env/bin python3
# -*- coding:utf-8 -*-
import threading
import time
import Jetson.GPIO as GPIO
from SensorI import SensorI
from SensorO import SensorO


class SensorsMgr:
    def __init__(self):
        self.i_size = 12
        self.o_size = 3
        self.started = False
        self.io_in = list[self.i_size]
        self.io_out = list[self.o_size]

        for i_num in range(0, self.i_size):
            self.io_in[i_num] = SensorI(i_num)
        for o_num in range(0, self.o_size):
            self.io_out[i_num] = SensorO(i_num)

        self.work_thread_i = threading.Thread(target=self.work_method_i)
        self.work_thread_i.start()
        self.work_thread_o = threading.Thread(target=self.work_method_o)
        self.work_thread_o.start()
        self.started = False
        self.pin_index_i = [7, 13, 15, 21, 23, 18, 22, 24, 26]
        self.pin_index_o = [19, 35, 36]
        self.init_gpio()

    def set_gpo(self, no, val):
        # value = (ushort)(val == 0 ? 1: 0)
        value = 0 if val == 0 else 1
        if 0 <= no < self.o_size:
            GPIO.output(self.pin_index_o[no], value)
            self.io_out[no].update_val(value)

    def get_sensor_i(self, no):
        if no < 0 or no > self.i_size:
            return None
        return self.io_in[no]

    def get_sensor_o(self, no):
        if no < 0 or no > self.o_size:
            return None
        return self.io_in[no]

    def init_gpio(self):
        for i_num in range(0, self.i_size):
            GPIO.setup(self.pin_index_i, GPIO.IN)

        for o_num in range(0, self.o_size):
            GPIO.setup(self.pin_index_o, GPIO.OUT)

    def get_jetson_i(self):
        # only servo signal
        # GPIO.setup(7, GPIO.IN)
        # GPIO.setup(13, GPIO.IN)
        # GPIO.setup(15, GPIO.IN)
        # GPIO.setup(21, GPIO.IN)
        # GPIO.setup(23, GPIO.IN)
        # GPIO.setup(18, GPIO.IN)
        # GPIO.setup(22, GPIO.IN)
        # GPIO.setup(24, GPIO.IN)
        # GPIO.setup(26, GPIO.IN)
        for i_num in range(0, self.i_size):
            value = GPIO.input(self.pin_index_i[i_num])
            if value:
                self.io_in[i_num].UpdateVal(1)
            else:
                self.io_in[i_num].UpdateVal(0)

        # 轴状态
        # 伺服报警、正硬极限、负硬极限、原点、正软限位、负软限位
        # int[] pos = {0, 1, 2, 4, 6, 7};
        # for (ushort i = 0; i < 21; i++)
        #     vals = Aixs[i].AxisIoStatus();
        #     for (var j = 0; j < 6; j++)
        #         uint val = (uint)1 << pos[j];
        #     if ((vals & val) == val)
        #         IO_IN[i * 6 + j + 64].UpdateVal(1);
        #     else
        #         IO_IN[i * 6 + j + 64].UpdateVal(0);

    # 虚拟IO 190~193
    def get_vir_i(self):
        pass

    def clear(self):
        for i_num in range(0, self.i_size):
            self.io_in[i_num].clear()

        for o_num in range(0, self.o_size):
            self.io_out[o_num].clear()

    def start(self):
        if ~self.started:
            self.started = True
            self.clear()
            self.work_thread_i.start()
            self.work_thread_o.start()

    def stop(self):
        if self.started:
            self.started = False
            self.work_thread_i = threading.Thread(target=self.work_thread_o)
            self.work_thread_o = threading.Thread(target=self.work_thread_i)

    def work_method_i(self):
        while self.started:
            self.get_jetson_i()
            # GetDMC3000_I()
            # GetVir_I()
            # for (int i = 0; i < I_SIZE; i++)
            #     IO_IN[i].DoWork()
            time.sleep(0.01)

    def work_method_o(self):
        while self.started:
            self.get_jetson_o()
            # for (int i = 0; i < O_SIZE; i++)
            #     IO_OUT[i].DoWork()
            time.sleep(0.01)
