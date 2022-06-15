################################################################################
#                                                                              #
#           pybricks script for 42109 - RC Truck v.3 by ufotografol            #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Not used                                                           #
#   Port B: Steering with left and right limited                               #
#   Port C: Not used                                                           #
#   Port D: Drive motor                                                        #
#                                                                              #
################################################################################
# Rebrickable: https://rebrickable.com/mocs/MOC-57612/                         #
# Script base: https://racingbrick.com/2021/08/remote-control-for-control-sets #
#                -without-an-app-or-smartphone-pybricks/                       #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.1.0 15-06-2022                                                            #
#   2 speed "gearbox" added.                                                   #
# v0.0.1 15-06-2022                                                            #
#   Changed variable namings.                                                  #
#   Changelog added.                                                           #
#   Comment header added.                                                      #
#   Changed the way speed is handled within the while loop.                    #
# v0.0.0 14-06-2022                                                            #
#   First version.                                                             #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.tools import wait

# Initialize the motors.
steering = Motor(Port.B)
driving = Motor(Port.D, Direction.CLOCKWISE)

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
gear = 1
speed = 50

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Check if the right middle button is pressed to change gear and set the
    # speed accordingly.
    if Button.RIGHT in pressed:
        if gear is 1:
            remote.light.on(Color.RED)
            gear = 2
            speed = 100
            wait(100)
        else:
            remote.light.on(Color.BLUE)
            gear = 1
            speed = 50
            wait(100)

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