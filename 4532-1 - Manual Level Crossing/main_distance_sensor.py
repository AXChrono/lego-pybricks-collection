################################################################################
#                                                                              #
#              pybricks script for 4532-1 - Manual Level Crossing              #
#                                                                              #
# This script enables the LEGO® 4532-1 - Manual Level Crossing to be used with #
# the LEGO Powerd UP system   .                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: 45303-1 - WeDo 2.0 Medium Motor                                    #
#   Port B: 45303-1 - WeDo 2.0 Medium Motor (not yet implemented)              #
#   Port C: 88007-1 - Color & Distance Sensor                                  #
#   Port D: 88007-1 - Color & Distance Sensor (not yet implemented)            #
#                                                                              #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.0.1 05-02-2023                                                            #
#   Add comments and header.                                                   #
# v0.0.0 04-02-2023                                                            #
#   First version.                                                             #
################################################################################

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, DCMotor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait

# variables to set
barrier_duty_cycle = 27 # speed of the motor (0-100).
barrier_wait = 575      # Time the barrier needs to go up or down in ms.
barrier_wait_up = 2000  # Time the barries waits to go up after last detection.

# Initialize the hub.
hub = TechnicHub()

# Initialize a the motors
barrier_motor_1 = DCMotor(Port.A)
#barrier_motor_2 = DCMotor(Port.B)
# Initialize the sensors.
distance_sensor_1 = ColorDistanceSensor(Port.C)
#distance_sensor_2 = ColorDistanceSensor(Port.D)

# Make the barrier go down to calibrate the position
barrier_motor_1.dc(barrier_duty_cycle)
# Wait for the amount of time set with "barrier_wait" plus an extra amount for calibration.
wait(barrier_wait+100)
# Stop the motor.
barrier_motor_1.stop()

# Wait a few milliseconds for the next step.
wait(10)

# Variable initialisation for further use.
wait_cycles=0        # number of cycles through the while loop before opening the barrier
barrier_position = 1 # Current barrier position (1=down, 0=up)

# Start program loop
while True:
    # Check to see if there is a train.
    if distance_sensor_1.distance() <= 40:
        # Change light color on hub to reflect the current status.
        hub.light.on(Color.RED)
        # Only send the barrier down if it's currently up.
        if barrier_position == 0:
            # Send barrier down.
            barrier_motor_1.dc(barrier_duty_cycle)
            # wait for the barrier to move to its position.
            wait(barrier_wait)
            # Stop the barrier from moving after the wait time.
            barrier_motor_1.stop()
            # Set the variable to the up position
            barrier_position = 1
        # As long as there is a train detected keep program within this loop.
        while distance_sensor_1.distance() <= 40:
            wait (10)
        # Set the number of while cycles to wait before sending the barrier up after last detection.
        wait_cycles = barrier_wait_up
    # Check if the barrier needs to stay down
    elif wait_cycles > 0:
        # Change light color on hub to reflect the current status.
        hub.light.on(Color.BLUE)
        # Change the number of cycles left before sending the barrier up.
        wait_cycles = wait_cycles-1
    # If there is no train and there is no need to keep the barrier down send it up.
    else:
        # Change light color on hub to reflect the current status.
        hub.light.on(Color.GREEN)
        # Only send the barrier up if it's currently down.
        if barrier_position == 1:
            # Send barrier down.
            barrier_motor_1.dc(-barrier_duty_cycle)
            # wait for the barrier to move to its position.
            wait(barrier_wait)
            # Stop the barrier from moving after the wait time.
            barrier_motor_1.stop()
            # Set the variable to the up position
            barrier_position = 0
        # As long as there is no train detected keep program within this loop.
        while distance_sensor_1.distance() > 40:
            wait (10)
    # wait for 1ms before continuing.
    wait(1)