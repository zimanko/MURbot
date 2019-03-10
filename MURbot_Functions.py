#from di_sensors import BNO055
import brickpi3
import math
import time
import MURbot_GUIclasses as MG
import evdev as ED


'''Global variables'''
BP = brickpi3.BrickPi3()
#BN = BNO055.BNO055()
LWP = 0						# Left wheel power; negative means forward
RWP = 0						# Right wheel power; negative means forward
HEADING = 0					# in degrees
SPEED = [time.time(), 0]
TILT = 30                   # tilting distance in cm
CURRENT_OBS_DATA = []
RADARDATA = []              # [[time, MB_pos, data], [time, MB_pos, data]]



'''MURbot Robotic Functions'''
def reset_all():
    global LWP, RWP
    LWP = 0
    RWP = 0
    BP.set_motor_power(BP.PORT_B, LWP)
    BP.set_motor_power(BP.PORT_C, RWP)
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
    BP.set_motor_position(BP.PORT_A, 0)
    BP.set_motor_position(BP.PORT_D, 0)
    print('Done')

    # Setup Ultrasonic sensors
    print('Setup Ultrasonic sensors...', end="")
    BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
    print('Done')

    # Calibrate IMU Sensor
    print('Calibrate IMU Sensor...', end="")
    while BN.get_calibration_status().count(3) != 4:
        BN.set_calibration(BN.get_calibration())
    print('Done')
    input('Put down the wehicle and press Enter')
    
    # Calibrate Heading to North
    print('Calibrate Heading to North...', end="")
    start_time = int(time.time())
    while (int(time.time()) - start_time) < 3:
        BN.read_euler()[0]
    global HEADING
    HEADING = BN.read_euler()[0]
    print('Done (' + str(HEADING) + ')')
    
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
		
		if BP.get_sensor(BP.PORT_3) < TILT and power < 0:
			power = 0
		elif BP.get_sensor(BP.PORT_1) < TILT and power > 0:
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


def move():
	global LWP, RWP
	
	if LWP < 0 and RWP < 0:
		while BP.get_sensor(BP.PORT_3) > TILT:
			BP.set_motor_power(BP.PORT_B, LWP)
			BP.set_motor_power(BP.PORT_C, RWP)
			#print('Power: ' + str(power))
			speed_and_orientation()
	elif LWP > 0 and RWP > 0:
		while BP.get_sensor(BP.PORT_1) > TILT:
			BP.set_motor_power(BP.PORT_B, LWP)
			BP.set_motor_power(BP.PORT_C, RWP)
			#print('Power: ' + str(power))
			speed_and_orientation()
	else:
		print('Opposing power signs!')
	LWP = 0
	RWP = 0
	BP.set_motor_power(BP.PORT_B, LWP)
	BP.set_motor_power(BP.PORT_C, RWP)
	speed_and_orientation()


def turn(turn_to):
	global LWP, RWP, HEADING
	print('turn started')

	def turn_clockwise():
		while True:
			curr_heading = BN.read_euler()[0]
			if curr_heading > (turn_to + 0.5) or curr_heading < (turn_to - 0.5):
				BP.set_motor_power(BP.PORT_B, -LWP)
				BP.set_motor_power(BP.PORT_C, RWP)
				print('clk Orientation: ' + str(BN.read_euler()[0]))
			else:
				break

	def turn_counter_clockwise():
		while True:
			curr_heading = BN.read_euler()[0]
			if curr_heading > (turn_to + 0.5) or curr_heading < (turn_to - 0.5):
				BP.set_motor_power(BP.PORT_B, LWP)
				BP.set_motor_power(BP.PORT_C, -RWP)
				print('coclk Orientation: ' + str(BN.read_euler()[0]))
			else:
				break

	LWP = 30
	RWP = 30
	turn_value = turn_to - BN.read_euler()[0]
	print(turn_value)
	
	BP.set_motor_position(BP.PORT_D, 285)
	
	if turn_value > -180 and turn_value < 0:
			turn_counter_clockwise()
	elif turn_value > 180:
			turn_counter_clockwise()
	elif turn_value > 0 and turn_value < 180:
			turn_clockwise()
	elif turn_value < -180:
			turn_clockwise()
	else:
		print('Something went wrong')
	
	print('turn ended')
	
	HEADING = BN.read_euler()[0]
	LWP = 0
	RWP = 0
	BP.set_motor_power(BP.PORT_B, LWP)
	BP.set_motor_power(BP.PORT_C, RWP)
	BP.set_motor_position(BP.PORT_D, 0)


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
	global HEADING
	MG.NavCanvas(MG.CANVAS_W, MG.SCALE_W)
	#move(-30, -30)
	#turn(0)

