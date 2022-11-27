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

    print("thymo: ", thymioDistanceSensor.getValue())
    print("custom: ", customDistanceSensor.getValue())



rows = zip(thymio_sensor, lower_sensor)

with open("../../results/simple_runner.csv", "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
