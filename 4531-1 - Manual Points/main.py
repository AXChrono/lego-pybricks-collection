################################################################################
#                                                                              #
#               pybricks script for Motorized 4531 Manual Points               #
#                                                                              #
# This script enables the LEGO® Powered Up Technic Hub to be used with the     #
# LEGO® Powerd UP 88010 Remote in conjunction with the 4531 Manual Points      #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: Track switch with left and right limited [optional                 #
#   Port B: Track switch with left and right limited [optional                 #
#   Port C: Track switch with left and right limited [optional                 #
#   Port D: Track switch with left and right limited [optional                 #
#                                                                              #
################################################################################
# Initial idea for the hardware: https://youtu.be/qWDMIOtVFSY                  #
################################################################################
# LEGO® is a trademark of the LEGO Group of companies which does not sponsor,  #
# authorize or endorse this project.                                           #
################################################################################

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.tools import wait
from uerrno import ENODEV

# Variables
used_ports = ["A", "B", "C", "D"] # Port names
track_switch = [0, 0, 0, 0] # Variable to initialize track switch
track_switch_left_end = [0, 0, 0, 0] # Left angle of switch track
track_switch_right_end = [0, 0, 0, 0] # Right angle of switch track
track_switch_angle = [0, 0, 0, 0] # Delta angle of switch track
switch_track_switch = [0, 0, 0, 0] # Will be set to 1 if track switch should be switched

# Test which port(s) have a motor connected.
x = 0
while x < 4:
    try:
        if x == 0:
            track_switch[x] = Motor(Port.A, Direction.CLOCKWISE)
        elif x == 1:
            track_switch[x] = Motor(Port.B, Direction.CLOCKWISE)
        elif x == 2:
            track_switch[x] = Motor(Port.C, Direction.CLOCKWISE)
        elif x == 3:
            track_switch[x] = Motor(Port.D, Direction.CLOCKWISE)
        print("Detected a motor on port " + used_ports[x] + ".")
    # if no motor is connected catch the error so the program wont stop.
    except OSError as ex:
        if ex.errno == ENODEV:
            print("There is no motor on port " + used_ports[x] + ".")
        else:
            print("An error occurred on port " + used_ports[x] + ".")
    x = x + 1

# Connect to the remote.
remote = Remote()

# Initialize the hub.
hub = TechnicHub()

# Find the switch track angles.
x = 0
while x < 4:
    if track_switch[x] != 0:
        # Find the endpoint on the left and right.
        # The middle is in between.
        track_switch_left_end[x] = track_switch[x].run_until_stalled(
            -200, then=Stop.HOLD
        )
        track_switch_right_end[x] = track_switch[x].run_until_stalled(
            200, then=Stop.HOLD
        )

        # We are now at the right. Reset this angle to be half the difference.
        # That puts zero in the middle.
        track_switch[x].reset_angle(
            (track_switch_right_end[x] - track_switch_left_end[x]) / 2
        )
        # Set angle
        track_switch_angle[x] = (
            (track_switch_right_end[x] - track_switch_left_end[x]) / 2
        ) - 5
        track_switch[x].run_target(200, -track_switch_angle[x], Stop.COAST, False)
    x = x + 1

# Main program.
while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Check if the left plus button is pressed to change switch track(s)
    if Button.LEFT_PLUS in pressed:
        while Button.LEFT_PLUS in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [1, 0, 0, 0]

    # Check if the left minus button is pressed to change switch track(s)
    if Button.LEFT_MINUS in pressed:
        while Button.LEFT_MINUS in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [0, 1, 0, 0]

    # Check if the left middle button is pressed to change switch track(s)
    if Button.LEFT in pressed:
        while Button.LEFT in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [1, 1, 0, 0]

    # Check if the right plus button is pressed to change switch track(s)
    if Button.RIGHT_PLUS in pressed:
        while Button.RIGHT_PLUS in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [0, 0, 1, 0]

    # Check if the right minus button is pressed to change switch track(s)
    if Button.RIGHT_MINUS in pressed:
        while Button.RIGHT_MINUS in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [0, 0, 0, 1]

    # Check if the lerightft middle button is pressed to change switch track(s)
    if Button.RIGHT in pressed:
        while Button.RIGHT in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [0, 0, 1, 1]

    # Check if the center button is pressed to change switch track(s)
    if Button.CENTER in pressed:
        while Button.CENTER in pressed:
            # Button debounce
            wait(10)
            pressed = remote.buttons.pressed()
        switch_track_switch = [1, 1, 1, 1]

    # Change the actual switch tracks
    x = 0
    while x < 4:
        # Check is switch track should be switched
        if switch_track_switch[x] == 1:
            # Check if the switch track to change is actually present as tested
            # during initialization.
            if track_switch[x] != 0:
                # Check the current position of the switch track so that if the
                # switch was switched manually it will still be switched.
                if track_switch[x].angle() > 0:
                    track_switch[x].run_target(
                        200, -track_switch_angle[x], Stop.COAST, False
                    )
                else:
                    track_switch[x].run_target(
                        200, track_switch_angle[x], Stop.COAST, False
                    )
                switch_track_switch[x] = 0
        x = x + 1

    # Wait.
    wait(10)
