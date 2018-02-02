import time
from di_sensors.inertial_measurement_unit import InertialMeasurementUnit
from di_sensors import BNO055
import brickpi3

BP = brickpi3.BrickPi3()
imu = InertialMeasurementUnit()
BN = BNO055.BNO055()

# Calibration:
if BN.get_calibration_status().count(3) != 4:
    while True:
        BN.set_calibration(BN.get_calibration())
        # print(BN.get_calibration_status())
        if BN.get_calibration_status().count(3) == 4 and imu.read_linear_acceleration().count(0) == 3:
            break


def move(power):
    BP.set_motor_power(BP.PORT_B, power)
    BP.set_motor_power(BP.PORT_C, -power)
    # space = (4 - len(str(power))) * ' '
    # print ('Motor power set to:' + space + str(power) + '  |  Voltage: ' + str(BP.get_voltage_battery()))

p = 0
while p < 1:
    move(40)
    t = 0
    while t < 10:
        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        accel = imu.read_linear_acceleration()

        string_to_print = "Accelerometer X: {:.1f}  Y: {:.1f} Z: {:.1f}".format(accel[0], accel[1], accel[2])
        print(string_to_print)
        time.sleep(0.1)
        t += 1
    move(-40)
    t = 0
    while t < 10:
        # Read the magnetometer, gyroscope, accelerometer, euler, and temperature values
        accel = imu.read_linear_acceleration()

        string_to_print = "Accelerometer X: {:.1f}  Y: {:.1f} Z: {:.1f}".format(accel[0], accel[1], accel[2])
        print(string_to_print)
        time.sleep(0.1)
        t += 1
    move(0)
    p += 1

BP.reset_all()
