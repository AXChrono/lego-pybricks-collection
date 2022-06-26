################################################################################
#                                                                              #
#   pybricks script for DAKAR / TRIAL Truck 42114 B alternate model / Zetros   #
#                   killer by RM8 LEGO Garage - BrickGarage                    #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Drive motor                                                        #
#   Port B: Steering with left and right limited                               #
#   Port C: Drive motor                                                        #
#   Port D: Not used                                                           #
#                                                                              #
################################################################################
# Rebrickable: https://rebrickable.com/mocs/MOC-113177/                        #
# Script base: https://racingbrick.com/2021/08/remote-control-for-control-sets #
#                -without-an-app-or-smartphone-pybricks/                       #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.1.0 26-06-2022                                                            #
#   Added half speed for drive.                                                #
#   Added half angle for steering.                                             #
# v0.0.0 26-06-2022                                                            #
#   First version.                                                             #
#   Based on v0.0.0 22-06-2022 of 42129 B model 'Hot Trot' by Didumos          #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.tools import wait

# Initialize the motors.
steering = Motor(Port.B, Direction.CLOCKWISE)
driving_1 = Motor(Port.A, Direction.COUNTERCLOCKWISE)
driving_2 = Motor(Port.C, Direction.CLOCKWISE)

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
        if Button.RIGHT in pressed:
            steering.run_target(1400, -(steer_angle/4), Stop.HOLD, False)
        else:
            steering.run_target(1400, -steer_angle, Stop.HOLD, False)
    elif Button.RIGHT_PLUS in pressed:
        if Button.RIGHT in pressed:
            steering.run_target(1400, (steer_angle/4), Stop.HOLD, False)
        else:
            steering.run_target(1400, steer_angle, Stop.HOLD, False)
    else:
        steering.track_target(0)

    # Choose the drive speed based on the left controls.
    if Button.LEFT_MINUS in pressed:
        if Button.LEFT in pressed:
            driving_1.dc(50)
            driving_2.dc(50)
        else:
            driving_1.dc(100)
            driving_2.dc(100)
    elif Button.LEFT_PLUS in pressed:
        if Button.LEFT in pressed:
            driving_1.dc(-50)
            driving_2.dc(-50)
        else:
            driving_1.dc(-100)
            driving_2.dc(-100)
    else:
        driving_1.dc(0)
        driving_2.dc(0)

    # Wait.
    wait(10)