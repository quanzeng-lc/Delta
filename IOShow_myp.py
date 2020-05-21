from Sensors.SensorsMgr import SensorsMgr
import time
smgr=SensorsMgr()
smgr.init_gpio()
smgr.start()
while True:
    input_value = list()
    input_value.append(smgr.get_sensor_i(0).get_val())
    input_value.append(smgr.get_sensor_i(1).get_val())
    input_value.append(smgr.get_sensor_i(2).get_val())
    input_value.append(smgr.get_sensor_i(3).get_val())
    input_value.append(smgr.get_sensor_i(4).get_val())
    input_value.append(smgr.get_sensor_i(5).get_val())
    input_value.append(smgr.get_sensor_i(6).get_val())
    input_value.append(smgr.get_sensor_i(7).get_val())
    input_value.append(smgr.get_sensor_i(8).get_val())
    print(input_value[0], input_value[1], input_value[2], input_value[3], input_value[4], input_value[5], input_value[6], input_value[7], input_value[8])
    time.sleep(1)
smgr.stop()
