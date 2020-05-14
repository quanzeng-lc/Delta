#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from GPIOPara import GPIOPara


def main():
    GPIOPara.gpio_set()
    print("hello world!")


if __name__ == '__main__':
    main()
