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
sonarDistanceSensor = robot.getDevice("prox.sonar")
infraredDistanceSensor = robot.getDevice("prox.infrared")

sonarDistanceSensor.enable(timeStep)
infraredDistanceSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

sonar_sensor_white = []
infrared_sensor_white = []
actual_value_white = []

sonar_sensor_red = []
infrared_sensor_red = []
actual_value_red = []

sonar_sensor_darkred = []
infrared_sensor_darkred = []
actual_value_dark_red = []

sonar_sensor_glowing_red = []
infrared_sensor_glowing_red = []
actual_value_glowing_red = []

sonar_sensor_mirror = []
infrared_sensor_mirror = []
actual_value_mirror = []

whiteRange = range(0, 351)
redRange = range(444, 794)
greenRange = range(887, 1237)
blueRange = range(1330, 1680)
mirroredRange = range(1766, 2116)

count = 0


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
    else:
        return 0


while robot.step(timeStep) != -1:

    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)

    count += 1
    print(count)
    traveled_distance = calculate_travel_distance(count)
    print(traveled_distance)
    actual_distance = (traveled_distance * math.sin(math.radians(8.11))) / math.sin(math.radians(180 - 8.11 - 90))

    if count in whiteRange:
        sonar_sensor_white.append(sonarDistanceSensor.getValue())
        infrared_sensor_white.append(infraredDistanceSensor.getValue())
        actual_value_white.append(actual_distance)
    elif count in redRange:
        sonar_sensor_red.append(sonarDistanceSensor.getValue())
        infrared_sensor_red.append(infraredDistanceSensor.getValue())
        actual_value_red.append(actual_distance)
    elif count in greenRange:
        sonar_sensor_darkred.append(sonarDistanceSensor.getValue())
        infrared_sensor_darkred.append(infraredDistanceSensor.getValue())
        actual_value_dark_red.append(actual_distance)
    elif count in blueRange:
        sonar_sensor_glowing_red.append(sonarDistanceSensor.getValue())
        infrared_sensor_glowing_red.append(infraredDistanceSensor.getValue())
        actual_value_glowing_red.append(actual_distance)
    elif count in mirroredRange:
        sonar_sensor_mirror.append(sonarDistanceSensor.getValue())
        infrared_sensor_mirror.append(infraredDistanceSensor.getValue())
        actual_value_mirror.append(actual_distance)

    if count >= 2130:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

rows = zip(sonar_sensor_white, infrared_sensor_white, actual_value_white, sonar_sensor_red, infrared_sensor_red,
           actual_value_red, sonar_sensor_darkred, infrared_sensor_darkred, actual_value_dark_red,
           sonar_sensor_glowing_red, infrared_sensor_glowing_red, actual_value_glowing_red, sonar_sensor_mirror,
           infrared_sensor_mirror, actual_value_mirror)

with open("../../results/proximity.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["sonar_white", "infrared_white", "actual_white", "sonar_red", "infrared_red", "actual_red", "sonar_dark_red",
         "infrared_dark_red", "actual_dark_red", "sonar_glowing_red", "infrared_glowing_red", "actual_glowing_red", "sonar_mirror",
         "infrared_mirror",
         "actual_mirror"])
    for row in rows:
        writer.writerow(row)
