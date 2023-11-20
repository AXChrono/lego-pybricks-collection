################################################################################
#                                                                              #
#        pybricks script for 42100 Model C - Tracked Carrier by Nico71         #
#                       This script is for the rear hub                        #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Drive motor                                                        #
#   Port B: Not used                                                           #
#   Port C: Drive motor                                                        #
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
drive_1 = Motor(Port.A, Direction.CLOCKWISE)
outriggers = Motor(Port.C, Direction.CLOCKWISE)
drive_3 = Motor(Port.D, Direction.CLOCKWISE)

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

    drive_1_speed = 0
    outriggers_speed = 0
    drive_3_speed = 0

    # Choose the drive speed based on the top controls.
    if Button.LEFT_PLUS in pressed:
        drive_1_speed = 100
    elif Button.RIGHT_PLUS in pressed:
        drive_1_speed = -100

    # Choose the drive speed based on the middle controls.
    if Button.LEFT in pressed:
        outriggers_speed = 100
    elif Button.RIGHT in pressed:
        outriggers_speed = -100

    # Choose the drive speed based on the bottom controls.
    if Button.LEFT_MINUS in pressed:
        drive_3_speed = 100
    elif Button.RIGHT_MINUS in pressed:
        drive_3_speed = -100

    drive_1.dc(drive_1_speed)
    outriggers.dc(outriggers_speed)
    drive_3.dc(drive_3_speed)

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
