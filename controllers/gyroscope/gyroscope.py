"""Naive maze runner controller."""

from controller import Robot
import time
import csv

robot = Robot()

# Get simulation step length.
timeStep = int(robot.getBasicTimeStep())

maxMotorVelocity = 6

# motors
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")

# sensor
gyroscope = robot.getDevice("gyro")
gyroscope.enable(timeStep)

accelerometer = robot.getDevice("accelerometer")
accelerometer.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

gyroscope_values = []
accelerometer_values = []
while robot.step(timeStep) != -1:
    # x-axis; y-axis; z-axis in radiant/s
    gyroscope_values.append(gyroscope.getValues())
    # x-axis; y-axis; z-axis in meter/s^2
    accelerometer_values.append((accelerometer.getValues()))
    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)
    print(accelerometer.getValues())

"""
rows = zip(ground_sensor, central_sensor, outer_left_sensor)

with open("../../results/simple_runner.csv", "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
"""