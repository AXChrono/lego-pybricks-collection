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
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.1.0 05-07-2022                                                            #
#   restructured to the version at pybricks-projects on Github                 #
#    https://github.com/pybricks/pybricks-projects/blob/master/sets/technic/   #
#    42124-off-road-buggy/powered-up-remote/main.py                            #
#   Changed gearbox part.                                                      #
#    Button left can only shift down                                           #
#    Button right can only shift up                                            #
#    New variables to easily change the number of gears                        #
#   Added battery indicator with hub LED.                                      #
# v0.0.0 04-07-2022                                                            #
#   First version.                                                             #
#   Based on v0.2.0 02-07-2022 of 42109-1 - App-Controlled Top Gear Rally Car  #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.hubs import TechnicHub
from pybricks.tools import wait

# Initialize the motors.
steering = Motor(Port.B, Direction.CLOCKWISE)
driving = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# Connect to the remote.
remote = Remote()

# Initialize the hub.
hub = TechnicHub()

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
steering_angle = (((right_end - left_end)/2)-5)

# Set variable for gear
gear_total = 3                        # Total number of gears.
gear_old = None                       # Empty variable to set later on (keep
                                      #  empty!).
gear = 1                              # Gear at start (must be higher than 0 and
                                      #  lower or eaqual to gear_total).
gear_color = ["BLUE", "WHITE", "RED"] # Number of colors should at least be
                                      #  equal to gear_total.

# Battery variables
voltage_current = hub.battery.voltage()
voltage = voltage_current

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Choose the steering angle based on the right controls.
    if Button.RIGHT_PLUS in pressed:
        steering.run_target(1400, -steering_angle, Stop.HOLD, False)
    elif Button.RIGHT_MINUS in pressed:
        steering.run_target(1400, steering_angle, Stop.HOLD, False)
    else:
        steering.track_target(0)

    # Check if the left middle button is pressed to change gear
    if Button.LEFT in pressed:
        if gear_old > 1:
            gear -= 1
        while Button.LEFT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    # Check if the right middle button is pressed to change gear
    if Button.RIGHT in pressed:
        if gear_old < gear_total:
            gear += 1
        while Button.RIGHT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    # Set speed according to the choosen gear.
    if gear is not gear_old:
        remote.light.on(Color[gear_color[gear-1]])
        speed = (100/gear_total)*gear
        gear_old = gear

    # Choose the drive speed based on the left controls.
    drive_speed = 0
    if Button.LEFT_PLUS in pressed:
        drive_speed += speed
    elif Button.LEFT_MINUS in pressed:
        drive_speed -= speed

    # Apply the selected speed.
    driving.dc(drive_speed)
    
    # Show battery status by hub LED.
    # Get current voltage and gradually up or down the value.
    voltage_current = hub.battery.voltage()
    if voltage_current < voltage:
        voltage -= 1
    elif voltage_current > voltage:
        voltage += 1
    # Show the correct color.
    if voltage > 9000:
        hub.light.on(Color.GREEN)
    elif voltage > 8100:
        hub.light.on(Color.YELLOW)
    elif voltage > 7200:
        hub.light.on(Color.ORANGE)
    else:
        hub.light.on(Color.RED)

    # Wait.
    wait(10)
