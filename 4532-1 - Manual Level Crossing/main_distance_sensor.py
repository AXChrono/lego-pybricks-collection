################################################################################
#                                                                              #
#              pybricks script for 4532-1 - Manual Level Crossing              #
#                                                                              #
# This script enables the LEGO® 4532-1 - Manual Level Crossing to be used with #
# the LEGO Powerd UP system   .                                                #
#                                                                              #
# Configuration of the Technic Hub:                                            #
#   Port A: 45303-1 - WeDo 2.0 Medium Motor                                    #
#   Port B:                                                                    #
#   Port C: 88007-1 - Color & Distance Sensor or                               #
#           45304-1 - WeDo 2.0 Motion Sensor                                   #
#   Port D: 88007-1 - Color & Distance Sensor or                               #
#           45304-1 - WeDo 2.0 Motion Sensor                                   #
#                                                                              #
################################################################################
#                                                                              #
#                                   Changelog                                  #
#                                                                              #
################################################################################
# v0.0.5 08-03-2023                                                            #
#   Combined distance_sensor_1 and _2 into an array (distance_sensor)          #
#   Added test for 2 sensor types on port C and D                              #
#   Changed value of barrier_wait_after                                        #
#   changed value of detection_distance                                        #
#   changed value of barrier_wait_up                                           #
# v0.0.4 01-03-2023                                                            #
#   Changed value of barrier_wait_up                                           #
#   Changed barrier_duty_cycle to barrier_duty_cycle_up                        #
#   Added variable barrier_duty_cycle_down                                     #
#   Added variable detection_distance                                          #
# v0.0.3 22-02-2023                                                            #
#   Changed values of barrier_duty_cycle, barrier_wait_up & barrier_wait_up    #
# v0.0.2 06-02-2023                                                            #
#   Changed barrier_wait_up to barrier_wait_after                              #
#   Changed barrier_wait to barrier_wait_up                                    #
#   Changed barrier_motor_1 to barrier_motor                                   #
#   Added barrier_wait_down                                                    #
# v0.0.1 05-02-2023                                                            #
#   Add comments and header.                                                   #
# v0.0.0 04-02-2023                                                            #
#   First version.                                                             #
################################################################################

from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, DCMotor, InfraredSensor, ColorDistanceSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait
from uerrno import ENODEV

# variables to set
barrier_duty_cycle_up = 50   # speed of the motor (0-100).
barrier_duty_cycle_down = 25 # speed of the motor (0-100).
barrier_wait_up = 1000        # Time the barrier needs to go up in ms.
barrier_wait_down = 750      # Time the barrier needs to go down in ms.
barrier_wait_after = 1000    # Time the barrier waits to go up after last detection.
detection_distance = 90      # Max distance for detection (0-100)

# Initialize the hub.
hub = TechnicHub()

# Initialize a the motor
barrier_motor = DCMotor(Port.A)

# Initialize the sensors.
distance_sensor = []
try:
    # Try to initialize a infrared sensor sensor on port C.
    distance_sensor.append(InfraredSensor(Port.C))
    print("Detected a infrared sensor on port C.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no infrared sensor on port C.")
    else:
        print("Another error occurred.")

try:
    # Try to initialize a color and distance sensor on port C.
    distance_sensor.append(ColorDistanceSensor(Port.C))
    print("Detected a color and distance sensor on port C.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no color and distance sensor on port C.")
    else:
        print("Another error occurred.")

try:
    # Try to initialize a infrared sensor sensor on port D.
    distance_sensor.append(InfraredSensor(Port.D))
    print("Detected a infrared sensor on port D.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no infrared sensor on port D.")
    else:
        print("Another error occurred.")

try:
    # Try to initialize a color and distance sensor on port D.
    distance_sensor.append(ColorDistanceSensor(Port.D))
    print("Detected a color and distance sensor on port D.")
except OSError as ex:
    if ex.errno == ENODEV:
        print("There is no color and distance sensor on port D.")
    else:
        print("Another error occurred.")


# Make the barrier go down to calibrate the position
barrier_motor.dc(-barrier_duty_cycle_down)
# Wait for the amount of time set with "barrier_wait_down" plus an extra amount for calibration.
wait(barrier_wait_down+100)
# Stop the motor.
barrier_motor.stop()

# Wait a few milliseconds for the next step.
wait(10)

# Variable initialisation for further use.
wait_cycles=0        # number of cycles through the while loop before opening the barrier
barrier_position = 1 # Current barrier position (1=down, 0=up)

# Start program loop
while True:
    # Check to see if there is a train.
    if distance_sensor[0].distance() <= detection_distance or distance_sensor[1].distance() <= detection_distance:
        # Change light color on hub to reflect the current status.
        hub.light.on(Color.RED)
        # Only send the barrier down if it's currently up.
        if barrier_position == 0:
            # Send barrier down.
            barrier_motor.dc(-barrier_duty_cycle_down)
            # wait for the barrier to move to its position.
            wait(barrier_wait_down)
            # Stop the barrier from moving after the wait time.
            barrier_motor.stop()
            # Set the variable to the up position
            barrier_position = 1
        # As long as there is a train detected keep program within this loop.
        while distance_sensor[0].distance() <= detection_distance or distance_sensor[1].distance() <= detection_distance:
            wait (10)
        # Set the number of while cycles to wait before sending the barrier up after last detection.
        wait_cycles = barrier_wait_after
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
            # Send barrier up.
            barrier_motor.dc(barrier_duty_cycle_up)
            # wait for the barrier to move to its position.
            wait(barrier_wait_up)
            # Stop the barrier from moving after the wait time.
            barrier_motor.stop()
            # Set the variable to the up position
            barrier_position = 0
        # As long as there is no train detected keep program within this loop.
        while distance_sensor[0].distance() > detection_distance and distance_sensor[1].distance() > detection_distance:
            wait (10)
    # wait for 1ms before continuing.
    wait(1)