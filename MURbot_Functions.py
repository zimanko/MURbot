from di_sensors import BNO055
import brickpi3
import math
import time
import MURbot_GUIclasses as MG


'''Global variables'''
BP = brickpi3.BrickPi3()
BN = BNO055.BNO055()
POWER = 0
HEADING = 0                 #in degrees
SPEED = [time.time(), 0]
TILT = 30                   #tilting distance in cm


'''MURbot Robotic Functions'''
def reset_all():
    move(0)
    BP.set_motor_position(BP.PORT_D, 0)
    BP.reset_all()


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
    BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
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
    while BP.get_sensor(BP.PORT_3) > TILT:
        BP.set_motor_power(BP.PORT_B, power)
        BP.set_motor_power(BP.PORT_C, -power)
        # print('Power: ' + str(power))
        # speed_and_orientation()
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    time.sleep(0.5)


def turn(degree):
    heading_start = BN.read_euler()[0]
    heading_end = heading_start + degree
    BP.set_motor_position(BP.PORT_D, 285)
    while abs(heading_end - BN.read_euler()[0]) < 0:
            BP.set_motor_power(BP.PORT_B, 0)
            BP.set_motor_power(BP.PORT_C, -power)
            print('Orientation: ' + BN.read_euler()[0])
        BP.set_motor_power(BP.PORT_B, 0)
        BP.set_motor_power(BP.PORT_C, 0)

    BP.set_motor_position(BP.PORT_D, 0)
    time.sleep(0.5)


def speed_and_orientation():
    global SPEED
    initial_speed = SPEED[1]
    heading = BN.read_euler()
    a = BN.read_linear_acceleration() * 100
    acc = a[1]
    if acc < -10 or acc > 10:
        acc = 0        
    t1 = time.time()
    SPEED[1] = round(initial_speed + acc * (t1 - SPEED[0]), 2)
    SPEED[0] = t1
    print('Speed: ' + str(SPEED[1]) + ' m/s  |  Heading: ' + str(heading[0]) + '  |  Y-acc: ' + str(acc))


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


def run():
    global POWER
    POWER = 10
    try:
        while True:
            move(POWER)
            turn('Left', 60)
    except KeyboardInterrupt:
        reset_all()



