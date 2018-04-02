from di_sensors import BNO055
import brickpi3
import math
import time
import MURbot_GUIclasses as MG
import MURbot_main as Mm


'''Global variables'''
BP = brickpi3.BrickPi3()
BN = BNO055.BNO055()
POWER = 0
HEADING = 0                 #in degrees
SPEED = [0, 0]


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
    #print('Power: ' + str(power))
    speed_and_orientation()
    return power


def turn(direction):
    if direction == 'Left':
        BP.set_motor_position(BP.PORT_D, 250)
    if direction == 'Right':
        BP.set_motor_position(BP.PORT_D, -250)
    if direction == 'Straight':
        BP.set_motor_position(BP.PORT_D, 0)
    speed_and_orientation()
    #print('Direction: ' + direction)


def tilt(tilt_distance, direction, duration):
    # pass the motor power to the direction and it use the sign of the power to detect direction
    # duration: how long would the function run in seconds (any negative number means infinite)
    global HEADING
    timer = 0
    start = time.time()
    #print('Duration: ' + str(duration))
    while timer < duration or duration < 0:
        try:
            if direction > 0:
                S1_value = BP.get_sensor(BP.PORT_1)
                #print('S1: ' + str(S1_value), end=" ")
                if S1_value < tilt_distance:
                    #print('TILT')
                    break
            if direction < 0:
                S4_value = BP.get_sensor(BP.PORT_4)
                #print('S4: ' + str(S4_value), end=" ")
                if S4_value < tilt_distance:
                    #print('TILT')
                    break
        except:
            continue
        end = time.time()
        timer = round(end - start)
        #print('Timer: ' + str(timer))
        speed_and_orientation()
        time.sleep(0.1)


def speed_and_orientation():
    global SPEED
    initial_speed = SPEED[1]
    heading = BN.read_euler()
    acc = BN.read_linear_accelration()
    t1 = time.time()
    SPEED[1] = initial_speed + acc[1] * (t1 - SPEED[0]))
    SPEED[0] = t1
    print('Speed: ' + str(SPEED[1]) + ' cm/s')


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
    MG.NavCanvas(Mm.root)
    global POWER
    POWER = 30
    reverse = -1 * POWER
    try:
        while True:
            move(POWER)
            tilt(50, POWER, -1)
            move(0)
            time.sleep(0.5)
            turn('Right')
            time.sleep(0.5)
            move(reverse)
            tilt(50, reverse, 3)
            move(0)
            time.sleep(0.5)
            turn('Straight')
            time.sleep(0.5)
    except KeyboardInterrupt:
        reset_all()



