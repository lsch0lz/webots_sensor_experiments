"""Naive maze runner controller."""
import math

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

thymioDistanceSensor.enable(timeStep)
laserDistanceSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

thymio_sensor = []
laser_sensor = []
actual_value = []

count = 0

whiteRange = range(0, 351)
redRange = range(444, 794)
greenRange = range(887, 1237)
blueRange = range(1330, 1680)
mirroredRange = range(1766, 2116)


def calculate_travel_distance(count):
    if count in whiteRange:
        return (99 / 35000) * count - (99 / 35000)
    elif count in redRange:
        return (99 / 35000) * (count - 444) - (99 / 35000)
    elif count in greenRange:
        return (99 / 35000) * (count - 887) - (99 / 35000)
    elif count in blueRange:
        return (99 / 35000) * (count - 1330) - (99 / 35000)
    elif count in mirroredRange:
        return (99 / 35000) * (count - 1766) - (99 / 35000)


while robot.step(timeStep) != -1:

    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)

    count += 1

    if count in whiteRange or count in redRange or count in greenRange or count in blueRange or count in mirroredRange:
        traveled_distance = calculate_travel_distance(count)
        actual_distance = (traveled_distance * math.sin(math.radians(8.11))) / math.sin(math.radians(180 - 8.11 - 90))

        print(actual_distance)

        thymio_sensor.append(thymioDistanceSensor.getValue())
        laser_sensor.append(laserDistanceSensor.getValue())
        actual_value.append(actual_distance)

    if count >= 2130:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

rows = zip(thymio_sensor, laser_sensor, actual_value)

with open("../../results/proximity.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["thymio", "laser", "perfect"])
    for row in rows:
        writer.writerow(row)
