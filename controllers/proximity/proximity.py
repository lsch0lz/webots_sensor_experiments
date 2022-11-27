"""Naive maze runner controller."""

from controller import Robot
import time
import csv

robot = Robot()

# Get simulation step length.
timeStep = int(robot.getBasicTimeStep())

maxMotorVelocity = 6

# motors
leftMotor = robot.getDevice("motor.left")
rightMotor = robot.getDevice("motor.right")

# front sensors
thymioDistanceSensor = robot.getDevice("prox.thymio")
customDistanceSensor = robot.getDevice("prox.custom")

thymioDistanceSensor.enable(timeStep)
customDistanceSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

thymio_sensor = []
lower_sensor = []

count = 0
while robot.step(timeStep) != -1:
    # always drive forward
    
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)

    thymio_sensor.append(thymioDistanceSensor.getValue())
    lower_sensor.append(customDistanceSensor.getValue())

    count += 1
    print(count)

    if (count >= 2650):
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

rows = zip(thymio_sensor, lower_sensor)

with open("../../results/proximity.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["thymio", "custom"])
    for row in rows:
        writer.writerow(row)
