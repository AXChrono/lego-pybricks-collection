################################################################################
#                                                                              #
#           pybricks script for 42114-1 - 6x6 Volvo Articulated Hauler         #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Drive motor                                                        #
#   Port B: 4 seed gearbox with left and right limited                         #
#   Port C: Not used                                                           #
#   Port D: Steering with left and right limited                               #
#                                                                              #
################################################################################
# Rebrickable: https://rebrickable.com/sets/42114-1/                           #
# Script base: https://racingbrick.com/2021/08/remote-control-for-control-sets #
#                -without-an-app-or-smartphone-pybricks/                       #
################################################################################
#                                                                              #
#                         Works with the following MOCs                        #
#                                                                              #
################################################################################
# 42114 Volvo N10 6x4 Dump Truck - alternate build by timtimgo                 #
#   https://rebrickable.com/mocs/MOC-81210/                                    #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.0.0 20-06-2022                                                            #
#   First version.                                                             #
#   Based on v0.1.0 15-06-2022 of 42109 - RC Truck v.3 by ufotografol          #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.tools import wait

# Initialize the motors.
gearbox = Motor(Port.B, Direction.CLOCKWISE)
steering = Motor(Port.D, Direction.COUNTERCLOCKWISE)
driving = Motor(Port.A, Direction.CLOCKWISE)

# Connect to the remote.
remote = Remote()

# Read the current settings
old_kp, old_ki, old_kd, _, _ = gearbox.control.pid()
old_kp, old_ki, old_kd, _, _ = steering.control.pid()

# Set new values
gearbox.control.pid(kp=old_kp*4, kd=old_kd*0.4)
steering.control.pid(kp=old_kp*4, kd=old_kd*0.4)

#Find the gearing endpoints but keep trying if value is below threshold of 200.
gear_angle = 0
while gear_angle < 200:
    # Find the steering endpoint on the left and right.
    # The middle is in between.
    left_end_gearbox = gearbox.run_until_stalled(-200, then=Stop.HOLD)
    right_end_gearbox = gearbox.run_until_stalled(200, then=Stop.HOLD)

    # Set gearing angle
    gear_angle = (((right_end_gearbox - left_end_gearbox)/2)-5)
    print('Gear angle measured:',gear_angle)

# Find the steering endpoint on the left and right.
# The middle is in between.
left_end_steering = steering.run_until_stalled(-200, then=Stop.HOLD)
right_end_steering = steering.run_until_stalled(200, then=Stop.HOLD)

# Set gearing angle
# Real angle of gear mechanism is 270 degrees (135 both sides from center).
gear_angle = 270/2
gear_angle_1 = gear_angle
gear_angle_2 = gear_angle-(((gear_angle+gear_angle)/3)*1)
gear_angle_3 = gear_angle-(((gear_angle+gear_angle)/3)*2)
gear_angle_tipper = -gear_angle
print('Gear angle real:',gear_angle)
# Set steering angle
steer_angle = (((right_end_steering - left_end_steering)/2)-5)
print('steer angle:',steer_angle)

# We are now at the right. Reset this angle to be half the difference.
# That puts zero in the middle.
gearbox.reset_angle((right_end_gearbox - left_end_gearbox)/2)
gearbox.run_target(1400, gear_angle, Stop.HOLD, False)
steering.reset_angle((right_end_steering - left_end_steering)/2)
steering.run_target(speed=200, target_angle=0, wait=False)

# Set variable for gear
gear_old = 1
gear = 1

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Check if the right middle button is pressed to change gear
    if Button.RIGHT in pressed:
        if gear_old is 1:
            gear = 2
        elif gear_old is 2:
            gear = 3
        elif gear_old is 3:
            gear = 4
        else:
            gear = 1
        while Button.RIGHT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    # Check if the left middle button is pressed to change gear
    if Button.LEFT in pressed:
        if gear_old is 1:
            gear = 4
        elif gear_old is 2:
            gear = 1
        elif gear_old is 3:
            gear = 2
        else:
            gear = 3
        while Button.LEFT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    if gear is not gear_old:
        # Stop driving to preserve gears
        driving.dc(0)
        if gear is 1:
            remote.light.on(Color.BLUE)
            gearbox.run_target(1400, gear_angle_1, Stop.HOLD, False)
            if gear_old is 4:
                wait(500)
            gear_old = 1
        elif gear is 2:
            remote.light.on(Color.WHITE)
            gearbox.run_target(1400, gear_angle_2, Stop.HOLD, False)
            gear_old = 2
        elif gear is 3:
            remote.light.on(Color.RED)
            gearbox.run_target(1400, gear_angle_3, Stop.HOLD, False)
            gear_old = 3
        else:
            remote.light.on(Color.GREEN)
            gearbox.run_target(1400, gear_angle_tipper, Stop.HOLD, False)
            if gear_old is 1:
                wait(500)
            gear_old = 4
        # Wait before going on so changing gear won't happen while driving. 
        wait(250)

    # Choose the steering angle based on the right controls.
    if Button.RIGHT_MINUS in pressed:
        steering.run_target(1400, -steer_angle, Stop.HOLD, False)
    elif Button.RIGHT_PLUS in pressed:
        steering.run_target(1400, steer_angle, Stop.HOLD, False)
    else:
        steering.track_target(0)

    # Choose the drive speed based on the left controls.
    if Button.LEFT_MINUS in pressed:
        driving.dc(100)
    elif Button.LEFT_PLUS in pressed:
        driving.dc(-100)
    else:
        driving.dc(0)

    # Wait.
    wait(10)