from Sensors.SensorsMgr import SensorsMgr
import time
smgr=SensorsMgr()
smgr.init_gpio()
smgr.start()
for i in range(100):
    print(smgr.get_sensor_i(0).get_val())
    time.sleep(0.01)
smgr.stop()
