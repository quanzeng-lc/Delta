#!/usr/env/bin python3
# -*- coding-utf-8 -*-
from enum import Enum
import threading

class SensorType(Enum):
    Low = 1  # 低电平
    High = 2  # 高电平

class SensorO:
    #public delegate void SensorEventHandler(object param)
    def __init__(self, no):
        self.no = no
        self._val = -1
        self._set = -1
        self._type = -1
        self.lock = threading.RLock()

    # < summary >
    # 更新传感器状态
    # < / summary >
    # < param name = "val" >
    # < / param >
    def update_val(self, val):
        if val == 1: # 高电平
            self._type = SensorType.High
        else:
            self._type = SensorType.Low
        self._val = val

    # < summary >
    # 设置输出
    # < / summary >
    # < param name = "val" >
    # < / param >
    def set_val(self, val):
        try:
            self.lock.acquire()
            self._set = val
        finally:
            self.lock.release()

    def get_val(self):
        return self._val == 1


    def do_work(self):
        self.lock.acquire()
        if self._set != -1 and self._set != self._val:
        # SensorsMgr.Inst().SetGPO(no, _set);
            self._val = self._set
        _set = -1
        if self._type == SensorType.Low:
            #  foreach(var item in SensorLowEvent):
            #  item.Key(item.Value)
            pass
        elif self._type == SensorType.High:

            pass
            #  foreach (var item in SensorHighEvent)
            #  item.Key(item.Value)

    def clear(self):
        self._val = -1

