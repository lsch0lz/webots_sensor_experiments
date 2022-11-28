"""Naive maze runner controller."""

from controller import Robot
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
laserDistanceSensor = robot.getDevice("prox.laser")
perfectDistanceSensor = robot.getDevice("prox.perfect")

thymioDistanceSensor.enable(timeStep)
laserDistanceSensor.enable(timeStep)
perfectDistanceSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

thymio_sensor = []
laser_sensor = []
perfect_sensor = []

count = 0
traveled_distance = 0
while robot.step(timeStep) != -1:

    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)

    thymio_sensor.append(thymioDistanceSensor.getValue())
    laser_sensor.append(laserDistanceSensor.getValue())
    perfect_sensor.append(perfectDistanceSensor.getValue())

    count += 1

    if count >= 2650:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

rows = zip(thymio_sensor, laser_sensor, perfect_sensor)

with open("../../results/proximity.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["thymio", "laser", "perfect"])
    for row in rows:
        writer.writerow(row)
