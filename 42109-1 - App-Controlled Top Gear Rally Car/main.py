from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.tools import wait

# Initialize the motors.
steer = Motor(Port.B)
front = Motor(Port.D, Direction.COUNTERCLOCKWISE)

# Connect to the remote.
remote = Remote()

# Read the current settings
old_kp, old_ki, old_kd, _, _ = steer.control.pid()

# Set new values
steer.control.pid(kp=old_kp*4, kd=old_kd*0.4)

# Find the steering endpoint on the left and right.
# The middle is in between.
left_end = steer.run_until_stalled(-200, then=Stop.HOLD)
right_end = steer.run_until_stalled(200, then=Stop.HOLD)

# We are now at the right. Reset this angle to be half the difference.
# That puts zero in the middle.
steer.reset_angle((right_end - left_end)/2)
steer.run_target(speed=200, target_angle=0, wait=False)

# Set steering angle for the buggy
steer_angle = (((right_end - left_end)/2)-5)
print('steer angle:',steer_angle)

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Choose the steer angle based on the right controls.

    if Button.RIGHT_MINUS in pressed:
        steer.run_target(1400, -steer_angle, Stop.HOLD, False)
    elif Button.RIGHT_PLUS in pressed:
        steer.run_target(1400, steer_angle, Stop.HOLD, False)
    else:
        steer.track_target(0)

    # Choose the drive speed based on the left controls.
    drive_speed = 0
    if Button.LEFT_MINUS in pressed:
        drive_speed += 100
    if Button.LEFT_PLUS in pressed:
        drive_speed -= 100

    # Apply the selected speed.
    front.dc(drive_speed)

    # Wait.
    wait(10)