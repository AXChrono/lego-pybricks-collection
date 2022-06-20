################################################################################
#                                                                              #
#             pybricks script for 42099 B model 'Rocky' by Didumos             #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Drive motor                                                        #
#   Port B: Drive motor                                                        #
#   Port C: Steering with left and right limited                               #
#   Port D: Not used                                                           #
#                                                                              #
################################################################################
# Rebrickable: https://rebrickable.com/mocs/MOC-30630                          #
# Script base: https://racingbrick.com/2021/08/remote-control-for-control-sets #
#                -without-an-app-or-smartphone-pybricks/                       #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.0.0 20-06-2022                                                            #
#   First version.                                                             #
#   Based on v0.0.0 20-06-2022 of 42129 B model 'Hot Trot' by Didumos          #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.tools import wait

# Initialize the motors.
steering = Motor(Port.C, Direction.COUNTERCLOCKWISE)
driving_1 = Motor(Port.A, Direction.CLOCKWISE)
driving_2 = Motor(Port.B, Direction.CLOCKWISE)

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

# Set steering angle
steer_angle = (((right_end - left_end)/2)-5)
print('steer angle:',steer_angle)

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Choose the steering angle based on the right controls.
    if Button.RIGHT_MINUS in pressed:
        steering.run_target(1400, -steer_angle, Stop.HOLD, False)
    elif Button.RIGHT_PLUS in pressed:
        steering.run_target(1400, steer_angle, Stop.HOLD, False)
    else:
        steering.track_target(0)

    # Choose the drive speed based on the left controls.
    if Button.LEFT_MINUS in pressed:
        driving_1.dc(100)
        driving_2.dc(100)
    elif Button.LEFT_PLUS in pressed:
        driving_1.dc(-100)
        driving_2.dc(-100)
    else:
        driving_1.dc(0)
        driving_2.dc(0)

    # Wait.
    wait(10)