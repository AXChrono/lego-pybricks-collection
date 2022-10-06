################################################################################
#                                                                              #
#        pybricks script for 42100 Model C - Tracked Carrier by Nico71         #
#                       This script is for the front hub                       #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Not used                                                           #
#   Port B: Drive motor                                                        #
#   Port C: Not used                                                           #
#   Port D: Drive motor                                                        #
#                                                                              #
################################################################################
# Rebrickable: https://rebrickable.com/mocs/MOC-105180/                        #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.0.0 09-07-2022                                                            #
#   First version.                                                             #
################################################################################

from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button, Color
from pybricks.hubs import TechnicHub
from pybricks.tools import wait

# Initialize the motors.
tracks_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)
tracks_right = Motor(Port.B, Direction.CLOCKWISE)

# Connect to the remote.
remote = Remote()

# Initialize the hub.
hub = TechnicHub()

# Battery variables
voltage_current = hub.battery.voltage()
voltage = voltage_current

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    tracks_left_speed = 0
    tracks_right_speed = 0

    # Choose the drive speed based on the left controls.
    if Button.LEFT_PLUS in pressed:
        tracks_left_speed = 100
    elif Button.LEFT_MINUS in pressed:
        tracks_left_speed = -100

    # Choose the drive speed based on the right controls.
    if Button.RIGHT_PLUS in pressed:
        tracks_right_speed = 100
    elif Button.RIGHT_MINUS in pressed:
        tracks_right_speed = -100

    tracks_left.dc(tracks_left_speed)
    tracks_right.dc(tracks_right_speed)

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
