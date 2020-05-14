#!/usr/env/bin python3
# -*- coding-utf-8 -*-
from enum import Enum

class SensorType(Enum):
    Low = 1 # 低电平
    High = 2 # 高电平
    Redge = 3 # 上升沿
    Dedge = 4 # 下降沿
    Unknown = 5  # 未知状态


class SensorI:
    def __init__(self, no):
        self.no = -1
        self._val = -1
        self.type = SensorType.Unknown

    # < summary >
    # 更新传感器状态
    # < / summary >
    # < param name = "val" > < / param >
    def update_val(self, val):
        if self._val == -1:
            if val == 1: # 高电平
                _type = SensorType.Redge
            else:
                _type = SensorType.Dedge
        else:
            if self._val == 0:
                if val == 1:   # 高电平
                    _type = SensorType.Redge
                else:
                    _type = SensorType.Low
            else:
                if val == 1:    # 高电平
                    _type = SensorType.High
                else:
                    _type = SensorType.Dedge
        self._val = val

    # < summary >
    # 获取传感器状态
    # < / summary >
    # < returns >
    # true: 高电平 false: 低电平
    # < / returns >
    def get_val(self):
        return self._val == 1

    def clear(self):
        self._val = -1
