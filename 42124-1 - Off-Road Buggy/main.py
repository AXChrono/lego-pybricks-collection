################################################################################
#                                                                              #
#                 pybricks script for 42124-1 - Off-Road Buggy                 #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Drive motor                                                        #
#   Port B: Steering with left and right limited                               #
#   Port C: Not used                                                           #
#   Port D: Not used                                                           #
#                                                                              #
################################################################################
# Script base: https://racingbrick.com/2021/08/remote-control-for-control-sets #
#                -without-an-app-or-smartphone-pybricks/                       #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.0.0 04-07-2022                                                            #
#   First version.                                                             #
#   Based on v0.2.0 02-07-2022 of 42109-1 - App-Controlled Top Gear Rally Car  #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.tools import wait

# Initialize the motors.
steering = Motor(Port.B)
driving = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# Connect to the remote.
remote = Remote()

# Read the current settings
old_kp, old_ki, old_kd, _, _ = steering.control.pid()

# Set new values
steering.control.pid(kp=old_kp*4, kd=old_kd*0.4)

# Find the steering endpoint on the left and right.
# The middle is in between.
left_end = steering.run_until_stalled(-200, then=Stop.HOLD)
right_end = steering.run_until_stalled(200, then=Stop.HOLD)

# We are now at the right. Reset this angle to be half the difference.
# That puts zero in the middle.
steering.reset_angle((right_end - left_end)/2)
steering.run_target(speed=200, target_angle=0, wait=False)

# Set steering angle for the buggy
steer_angle = (((right_end - left_end)/2)-5)

# Set variable for gear
gear_old = 1
gear = 1
speed = 33

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Check if the right middle button is pressed to change gear
    if Button.RIGHT in pressed:
        if gear_old is 1:
            gear = 2
        elif gear_old is 2:
            gear = 3
        else:
            gear = 1
        while Button.RIGHT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    # Check if the left middle button is pressed to change gear
    if Button.LEFT in pressed:
        if gear_old is 3:
            gear = 2
        elif gear_old is 2:
            gear = 1
        else:
            gear = 3
        while Button.LEFT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    if gear is not gear_old:
        if gear is 1:
            remote.light.on(Color.BLUE)
            speed = 33
            gear_old = 1
        elif gear is 2:
            remote.light.on(Color.WHITE)
            speed = 67
            gear_old = 2
        else:
            remote.light.on(Color.RED)
            speed = 100
            gear_old = 3

    # Choose the steering angle based on the right controls.
    if Button.RIGHT_PLUS in pressed:
        steering.run_target(1400, -steer_angle, Stop.HOLD, False)
    elif Button.RIGHT_MINUS in pressed:
        steering.run_target(1400, steer_angle, Stop.HOLD, False)
    else:
        steering.track_target(0)

    # Choose the drive speed based on the left controls.
    if Button.LEFT_PLUS in pressed:
        driving.dc(speed)
    elif Button.LEFT_MINUS in pressed:
        driving.dc(-speed)
    else:
        driving.dc(0)

    # Wait.
    wait(10)
