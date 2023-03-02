from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.tools import wait
from uerrno import ENODEV

hub = TechnicHub()

track_switch = [0, 0, 0, 0]
track_switch_present = [0, 0, 0, 0]
track_switch_left_end = [0, 0, 0, 0]
track_switch_right_end = [0, 0, 0, 0]
track_switch_angle = [0, 0 ,0 ,0]

try:
    # Try to initialize a motor.
    track_switch[0] = Motor(Port.A, Direction.CLOCKWISE)
    track_switch_present[0] = 1
    print("Detected a motor on port A.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no motor on port B.")
    else:
        print("Another error occurred.")

try:
    # Try to initialize a motor.
    track_switch[1] = Motor(Port.B, Direction.CLOCKWISE)
    track_switch_present[1] = 1
    print("Detected a motor on port B.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no motor on port B.")
    else:
        print("Another error occurred.")

try:
    # Try to initialize a motor.
    track_switch[2] = Motor(Port.C, Direction.CLOCKWISE)
    track_switch_present[2] = 1
    print("Detected a motor on port C.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no motor on port C.")
    else:
        print("Another error occurred.")

try:
    # Try to initialize a motor.
    track_switch[3] = Motor(Port.D, Direction.CLOCKWISE)
    track_switch_present[3] = 1
    print("Detected a motor on port D.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no motor on port D.")
    else:
        print("Another error occurred.")

# Connect to the remote.
remote = Remote()

# Initialize the hub.
hub = TechnicHub()

x = 0
while x < 4:
    if track_switch_present[x] == 1:
        # Find the steering endpoint on the left and right.
        # The middle is in between.
        track_switch_left_end[x] = track_switch[x].run_until_stalled(-200, then=Stop.HOLD)
        track_switch_right_end[x] = track_switch[x].run_until_stalled(200, then=Stop.HOLD)

        # We are now at the right. Reset this angle to be half the difference.
        # That puts zero in the middle.
        track_switch[x].reset_angle((track_switch_right_end[x] - track_switch_left_end[x])/2)
        # Set steering angle
        track_switch_angle[x] = (((track_switch_right_end[x] - track_switch_left_end[x])/2)-5)
        track_switch[x].run_target(200, -track_switch_angle[x], Stop.COAST, False)
    x = x + 1

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Check if the left middle button is pressed to change gear
    if track_switch_present[0] == 1:
        if Button.LEFT_PLUS in pressed:
            while Button.LEFT_PLUS in pressed:
                # Button debounce 
                wait(10)
                pressed = remote.buttons.pressed()
            if track_switch[0].angle() > 0:
                track_switch[0].run_target(200, -track_switch_angle[0], Stop.COAST, False)
            else:
                track_switch[0].run_target(200, track_switch_angle[0], Stop.COAST, False)

    if track_switch_present[1] == 1:
        # Check if the left middle button is pressed to change gear
        if Button.LEFT_MINUS in pressed:
            while Button.LEFT_MINUS in pressed:
                # Button debounce 
                wait(10)
                pressed = remote.buttons.pressed()
            if track_switch[1].angle() > 0:
                track_switch[1].run_target(200, -track_switch_angle[1], Stop.COAST, False)
            else:
                track_switch[1].run_target(200, track_switch_angle[1], Stop.COAST, False)

    # Check if the left middle button is pressed to change gear
    if Button.LEFT in pressed:
        while Button.LEFT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()
        if track_switch_present[0] == 1:
            if track_switch[0].angle() > 0:
                track_switch[0].run_target(200, -track_switch_angle[0], Stop.COAST, False)
            else:
                track_switch[0].run_target(200, track_switch_angle[0], Stop.COAST, False)
        if track_switch_present[1] == 1:
            if track_switch[1].angle() > 0:
                track_switch[1].run_target(200, -track_switch_angle[1], Stop.COAST, False)
            else:
                track_switch[1].run_target(200, track_switch_angle[1], Stop.COAST, False)

    if track_switch_present[2] == 1:
        # Check if the left middle button is pressed to change gear
        if Button.RIGHT_PLUS in pressed:
            while Button.RIGHT_PLUS in pressed:
                # Button debounce 
                wait(10)
                pressed = remote.buttons.pressed()
            if track_switch[2].angle() > 0:
                track_switch[2].run_target(200, -track_switch_angle[2], Stop.COAST, False)
            else:
                track_switch[2].run_target(200, track_switch_angle[2], Stop.COAST, False)

    if track_switch_present[3] == 1:
        # Check if the left middle button is pressed to change gear
        if Button.RIGHT_MINUS in pressed:
            while Button.RIGHT_MINUS in pressed:
                # Button debounce 
                wait(10)
                pressed = remote.buttons.pressed()
            if track_switch[3].angle() > 0:
                track_switch[3].run_target(200, -track_switch_angle[3], Stop.COAST, False)
            else:
                track_switch[3].run_target(200, track_switch_angle[3], Stop.COAST, False)

    # Check if the left middle button is pressed to change gear
    if Button.RIGHT in pressed:
        while Button.RIGHT in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()
        if track_switch_present[2] == 1:
            if track_switch[2].angle() > 0:
                track_switch[2].run_target(200, -track_switch_angle[2], Stop.COAST, False)
            else:
                track_switch[2].run_target(200, track_switch_angle[2], Stop.COAST, False)
        if track_switch_present[3] == 1:
            if track_switch[3].angle() > 0:
                track_switch[3].run_target(200, -track_switch_angle[3], Stop.COAST, False)
            else:
                track_switch[3].run_target(200, track_switch_angle[3], Stop.COAST, False)

    # Check if the left middle button is pressed to change gear
    if Button.CENTER in pressed:
        while Button.CENTER in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()
        if track_switch_present[0] == 1:
            if track_switch[0].angle() > 0:
                track_switch[0].run_target(200, -track_switch_angle[0], Stop.COAST, False)
            else:
                track_switch[0].run_target(200, track_switch_angle[0], Stop.COAST, False)
        if track_switch_present[1] == 1:
            if track_switch[1].angle() > 0:
                track_switch[1].run_target(200, -track_switch_angle[1], Stop.COAST, False)
            else:
                track_switch[1].run_target(200, track_switch_angle[1], Stop.COAST, False)
        if track_switch_present[2] == 1:
            if track_switch[2].angle() > 0:
                track_switch[2].run_target(200, -track_switch_angle[2], Stop.COAST, False)
            else:
                track_switch[2].run_target(200, track_switch_angle[2], Stop.COAST, False)
        if track_switch_present[3] == 1:
            if track_switch[3].angle() > 0:
                track_switch[3].run_target(200, -track_switch_angle[3], Stop.COAST, False)
            else:
                track_switch[3].run_target(200, track_switch_angle[3], Stop.COAST, False)

    # Wait.
    wait(10)
