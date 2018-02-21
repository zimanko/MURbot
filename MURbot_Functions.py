import BNO055 # !! change to: from di_sensors import BNO055
import brickpi3
import math
import time

BP = brickpi3.BrickPi3()
BN = BNO055.BNO055()

# MURbot Functions:
def setup():
    # Set motor positioning in a high state
    print('Set motor positioning in a high state...', end="")
    BP.set_motor_position_kp(BP.PORT_A, 120)
    BP.set_motor_position_kd(BP.PORT_A, 100)
    BP.set_motor_position_kp(BP.PORT_D, 120)
    BP.set_motor_position_kd(BP.PORT_D, 100)
    print('Done')

    # Setup Ultrasonic sensors
    print('Setup Ultrasonic sensors...', end="")
    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    BP.set_sensor_type(BP.PORT_4, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    print('Done')

    # Calibrate IMU Sensor
    print('Calibrate IMU Sensor...', end="")
    rounds = 0
    while rounds < 100:
        BN.set_calibration(BN.get_calibration())
        status = BN.get_calibration_status().count(3)
        if status == 4:
            break
        if rounds > 10 and status == 3:
            break
        if rounds > 20 and status == 2:
            break
        rounds += 1
    print('Done (' + str(status) + ')')

    time.sleep(3)


def move(power):
    BP.set_motor_power(BP.PORT_B, power)
    BP.set_motor_power(BP.PORT_C, -power)
    return power


def turn(direction):
    if direction == 'Left':
        BP.set_motor_position(BP.PORT_D, 120)
    if direction == 'Right':
        BP.set_motor_position(BP.PORT_D, -120)
    if direction == 'Straight':
        BP.set_motor_position(BP.PORT_D, 0)


def tilt(tilt_distance, direction, duration):
    # pass the motor power to the direction and it use the sign of the power for detection direction
    # duration: how long would the function run in seconds (any negative number means infinite)
    timer = 0
    while timer < duration or duration < 0:
        start = time.time()
        try:
            if direction < 0:
                if BP.get_sensor(BP.PORT_1) < tilt_distance:
                    break
            if direction > 0:
                if BP.get_sensor(BP.PORT_4) < tilt_distance:
                    break
        except:
            continue
        end = time.time()
        timer = round(end - start)

def radar(dps, ch):
    BP.set_motor_dps(BP.PORT_A, dps)
    alpha = BP.get_motor_encoder(BP.PORT_A) * ch
    try:
        c1 = BP.get_sensor(BP.PORT_1)
        c2 = BP.get_sensor(BP.PORT_4)
    except:
        c1 = c2 = 0
    a1 = math.sin(alpha) * c1
    b1 = math.cos(alpha) * c1
    a2 = math.sin(alpha) * c2
    b2 = math.cos(alpha) * c2
    return a1, b1, a2, b2

def whatever():
    t = 0
    while t < 1:
        BP.set_motor_dps(BP.PORT_A, 80)
        while BP.get_motor_encoder(BP.PORT_A) < 530:
            alpha = BP.get_motor_encoder(BP.PORT_A) * ch
            try:
                c1 = BP.get_sensor(BP.PORT_1)
                c2 = BP.get_sensor(BP.PORT_4)
                # print ('OK at ' + str(alpha))
            except:
                c1 = c2 = 0
                # print('Sensor Error at ' + str(alpha))
            a1 = math.sin(alpha) * c1
            b1 = math.cos(alpha) * c1
            a2 = math.sin(alpha) * c2
            b2 = math.cos(alpha) * c2
            TR.setpos(-a1, b1)
            if c1 > 250:
                TR.dot(1, 'grey')
            else:
                TR.dot(10, 'blue')
            TR.setpos(a2, -b2)
            if c2 > 250:
                TR.dot(1, 'grey')
            else:
                TR.dot(10, 'blue')
            # time.sleep(0.2)
        BP.set_motor_dps(BP.PORT_A, -80)
        while BP.get_motor_encoder(BP.PORT_A) > 0:
            alpha = BP.get_motor_encoder(BP.PORT_A) * ch
            try:
                c1 = BP.get_sensor(BP.PORT_1)
                c2 = BP.get_sensor(BP.PORT_4)
                # print ('OK at ' + str(alpha))
            except:
                c1 = c2 = 0
                # print('Sensor Error at ' + str(alpha))
            a1 = math.sin(alpha) * c1
            b1 = math.cos(alpha) * c1
            a2 = math.sin(alpha) * c2
            b2 = math.cos(alpha) * c2
            if c1 > 250:
                TR.dot(1, 'grey')
            else:
                TR.dot(10, 'blue')
            TR.setpos(a2, -b2)
            if c2 > 250:
                TR.dot(1, 'grey')
            else:
                TR.dot(10, 'blue')
            # time.sleep(0.2)
        BP.set_motor_dps(BP.PORT_A, 0)
        t += 1

