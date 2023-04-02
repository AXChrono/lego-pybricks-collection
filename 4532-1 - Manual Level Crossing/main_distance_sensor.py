from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, DCMotor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()

barrier_duty_cycle = 27
barrier_wait = 575
barrier_wait_up = 2000

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

wait_cycles=0

barrier_position = 0

while True:
    if sensor.distance() <= 40:
        hub.light.on(Color.RED)
        if barrier_position == 0:
            example_motor.dc(barrier_duty_cycle)
            wait(barrier_wait)
            example_motor.stop()
            barrier_position = 1
        while sensor.distance() <= 40:
            wait (10)
        wait_cycles = barrier_wait_up/10
    elif wait_cycles > 0:
        #print((1/(barrier_wait_up/10))*wait_cycles)
        hub.light.on(Color.BLUE)
        wait_cycles = wait_cycles-1
    else:
        hub.light.on(Color.GREEN)
        if barrier_position == 1:
            example_motor.dc(-barrier_duty_cycle)
            wait(barrier_wait)
            example_motor.stop()
            barrier_position = 0
        while sensor.distance() > 40:
            wait (10)
    wait(10)