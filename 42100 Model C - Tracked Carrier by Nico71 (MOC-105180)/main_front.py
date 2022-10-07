################################################################################
#                                                                              #
#        pybricks script for 42100 Model C - Tracked Carrier by Nico71         #
#                       This script is for the front hub                       #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote.                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Drive motor                                                        #
#   Port B: Drive motor                                                        #
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
crane_top = Motor(Port.A, Direction.CLOCKWISE)
tracks_right = Motor(Port.B, Direction.CLOCKWISE)
engine = Motor(Port.C, Direction.CLOCKWISE)
tracks_left = Motor(Port.D, Direction.COUNTERCLOCKWISE)

# Connect to the remote.
remote = Remote()

# Initialize the hub.
hub = TechnicHub()

# Battery variables
voltage_current = hub.battery.voltage()
voltage = voltage_current

engine_speed_set = 25
engine_speed = 0

engine_fail_counter_set = 20
engine_fail_counter = engine_fail_counter_set

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    tracks_left_speed = 0
    tracks_right_speed = 0
    crane_top_speed = 0

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

    # Choose the drive speed based on the center controls.
    if Button.LEFT in pressed:
        crane_top_speed = 100
    elif Button.RIGHT in pressed:
        crane_top_speed = -100
    
    if Button.CENTER in pressed:
        if engine_speed is engine_speed_set or engine_speed is -engine_speed_set:
            engine_speed = 0
            engine_fail_counter = engine_fail_counter_set
        else:
            engine_speed = engine_speed_set
        while Button.CENTER in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()

    tracks_left.dc(tracks_left_speed)
    tracks_right.dc(tracks_right_speed)
    crane_top.dc(crane_top_speed)
    engine.dc(engine_speed)

    if engine_speed < 0 or engine_speed > 0:
        engine_speed_measured = engine.speed()

        if engine_speed_measured < 0:
            engine_speed_measured = -engine_speed_measured

        if engine_speed_measured < 100:
            if engine_fail_counter > 0:
                engine_fail_counter = engine_fail_counter-1
            else:
                engine_speed = -engine_speed
                engine_fail_counter = engine_fail_counter_set
        else:
            engine_fail_counter = engine_fail_counter_set

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
