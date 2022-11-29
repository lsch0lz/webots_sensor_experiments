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

ps0 = robot.getDevice("ps0")
ps0.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

count = 0

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
    
    if count > 100:
        velocity = 0.1
    
    if count > 150:
        velocity = 6
    
    if count == 420:
        break

    count += 1
    print(count)
for value in accelerometer_values:
    x_axis = value[0]
    y_axis = value[1]
    z_axis = value[2]
    with open("../../results/accelerometer.csv", "a") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([x_axis, y_axis, z_axis])
