from di_sensors import BNO055
import brickpi3
import math
import time
import MURbot_GUIclasses as MG
import evdev as ED


'''Global variables'''
BP = brickpi3.BrickPi3()
BN = BNO055.BNO055()
LWP = 0
RWP = 0
HEADING = 3 * math.pi / 2                #in degrees
SPEED = [time.time(), 0]
TILT = 30                   #tilting distance in cm
CURRENT_OBS_DATA = []
RADARDATA = []              #[[time, MB_pos, data], [time, MB_pos, data]]



'''MURbot Robotic Functions'''
def reset_all():
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    BP.set_motor_position(BP.PORT_D, 0)
    BP.set_motor_position(BP.PORT_A, 0)
    BP.reset_all()
    time.sleep(1.5)
    print('System stopped')


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
    print('Ready to go!')


def freeride():
	device = ED.InputDevice('/dev/input/event0')
	print('Input device: ' + str(device.name))
	power = 0 
	turn_value = 0
	
	for event in device.read_loop():
		if event.code == ED.ecodes.ABS_Y:
			power = int((event.value - 128) / 2)
		if event.code == ED.ecodes.ABS_Z:
			turn_value = int(event.value - 127.5)
			modifier = 1 - abs(turn_value / 250)
		BP.set_motor_position(BP.PORT_D, int(1.11 * turn_value))
		
		if BP.get_sensor(BP.PORT_3) > TILT:
			power = 0
		elif BP.get_sensor(BP.PORT_1) > TILT:
			power = 0
		else:
			rwp = power
			lwp = power
		
		if turn_value < 0:
			lwp = int(modifier * power)
		if turn_value > 0:
			rwp = int(modifier * power)
		
		BP.set_motor_power(BP.PORT_B, lwp)
		BP.set_motor_power(BP.PORT_C, rwp)
		
		speed_and_orientation()


def move(lwp, rwp):
    while BP.get_sensor(BP.PORT_3) > TILT:
        BP.set_motor_power(BP.PORT_B, lwp)
        BP.set_motor_power(BP.PORT_C, rwp)
        #print('Power: ' + str(power))
        speed_and_orientation()
    BP.set_motor_power(BP.PORT_B, 0)
    BP.set_motor_power(BP.PORT_C, 0)
    speed_and_orientation()

'''
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
'''

def speed_and_orientation():
    global SPEED
    initial_speed = SPEED[1]
    heading = BN.read_euler()
    acc = BN.read_linear_acceleration()[1]    
    if LWP == 0 and RWP == 0:
		acc = 0
    t1 = time.time()
    SPEED[1] = round(initial_speed + acc * (t1 - SPEED[0]), 2)
    SPEED[0] = t1
    print(acc, SPEED[1])


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
	#MG.NavCanvas(MG.CANVAS_W, MG.SCALE_W)
	#move(3-30, -30)
	while True:
		speed_and_orientation()




