from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, DCMotor, Remote, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

# Connect to the remote.
remote = Remote()

barrier_duty_cycle = 27
barrier_wait = 575

# Initialize a motor without rotation sensors on port A.
example_motor = DCMotor(Port.A)

# Initialize the sensor.
sensor = ColorDistanceSensor(Port.C)

# Make the motor go clockwise (forward) at 70% duty cycle ("70% power").
example_motor.dc(barrier_duty_cycle)

# Wait for three seconds.
wait(barrier_wait+100)

example_motor.stop()

wait(1000)

# Make the motor go counterclockwise (backward) at 70% duty cycle.
example_motor.dc(-barrier_duty_cycle)

# Wait for three seconds.
wait(barrier_wait)
example_motor.stop()

barrier_position = 0

while True:
    # Check which buttons are pressed.
    pressed = remote.buttons.pressed()

    # Show the result.
    #print("pressed:", pressed)

    # Check a specific button.
    #if Button.LEFT_PLUS in pressed:
    if sensor.distance() <= 40:
        while Button.LEFT_PLUS in pressed:
            # Button debounce 
            wait(10)
            pressed = remote.buttons.pressed()
        if barrier_position == 0:
            example_motor.dc(barrier_duty_cycle)
            barrier_position = 1
        else:
            example_motor.dc(-barrier_duty_cycle)
            barrier_position = 0
        wait(barrier_wait)
        example_motor.stop()
        while sensor.distance() <= 40:
            wait (10)



    # Wait so we can see the result.
    wait(100)