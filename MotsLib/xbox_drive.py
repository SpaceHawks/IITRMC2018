import xbox;
import comms;
import time;
import signal;
import sys;
import mots;


# make it so that when user ends manual control the robot is first told to stop moving
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!');
    comms.send([1, 10, 0, 0]);
    sys.exit(0);

signal.signal(signal.SIGINT, signal_handler);


# get the joystick speed from the xbox controller
def get_speed_turn(joy):
    x, y = joy.leftStick();
    print("x:%s, y:%s" % (x,y));
    speed = y * 100;
    turn = x * 100;
    return (speed, turn);

# send command to the robot
def send_drive_cmd(speed, turn):
	# convert speed + turn to l & r motor speeds
	v = (100 - abs(turn)) * (speed / 100) + speed;
	w = (100 - abs(speed)) * (turn / 100) + turn;
	l = (v + w) / 2;
	r = (v - w) / 2;
	# send tank drive command
    comms.send([1, 11, l, r]);


drill_status = 0;
drill_direction = 1;
auger = Auger();
# read buttons from xbox-controller
def control_auger(joy):
    # toggle buttons to control the auger
    if joy.A(): # toggle power
        drill_status = !drill_status;
    if joy.B(): # toggle direction
        drill_direction = -drill_direction;
    auger.set_drill(drill_status * drill_direction);


# xbox controller
joy = xbox.Joystick();


# main loop
while True:
    speed, turn = get_speed_turn(joy);
    send_drive_cmd(speed, turn);

    time.sleep(1 / 8); # 8 fps
