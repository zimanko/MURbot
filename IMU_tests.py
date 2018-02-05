import time
from di_sensors import BNO055
import brickpi3
import MURbot

BP = brickpi3.BrickPi3()
BN = BNO055.BNO055()

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

BP.set_motor_position_kp(BP.PORT_D, 120)
BP.set_motor_position_kd(BP.PORT_D, 100)

while BN.get_calibration_status().count(3) != 4:
    BN.set_calibration(BN.get_calibration())
    # print(BN.get_calibration_status())
    if BN.get_calibration_status().count(3) == 4:
        break

Tilt_dist = 40
Motor_power = 40
Turn = 0

while Turn < 5:
    BP.set_motor_position(BP.PORT_D, 0)
    while BP.get_sensor(BP.PORT_1) > Tilt_dist and BP.get_sensor(BP.PORT_4) > Tilt_dist:
        MURbot.move(Motor_power)
    MURbot.move(0)
    time.sleep(0.5)
    BP.set_motor_position(BP.PORT_D, 120)
    MURbot.move(-Motor_power / 2)
    time.sleep(1)
    MURbot.move(0)
    Motor_power = -1 * Motor_power
    Turn += 1

BP.reset_all()
