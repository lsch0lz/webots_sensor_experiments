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
laserDistanceSensor = robot.getDevice("prox.laser")
infraredDistanceSensor = robot.getDevice("prox.infrared")

laserDistanceSensor.enable(timeStep)
infraredDistanceSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

laser_sensor_white = []
infrared_sensor_white = []
actual_value_white = []

laser_sensor_red = []
infrared_sensor_red = []
actual_value_red = []

laser_sensor_darkred = []
infrared_sensor_darkred = []
actual_value_dark_red = []

laser_sensor_glowing_red = []
infrared_sensor_glowing_red = []
actual_value_glowing_red = []

laser_sensor_mirror = []
infrared_sensor_mirror = []
actual_value_mirror = []

whiteRange = range(0, 350)
redRange = range(354, 703)
darkRedRange = range(709, 1058)
glowingRedRange = range(1063, 1412)
mirroredRange = range(1416, 1770)

count = 0


def calculate_travel_distance(count):
    if count in whiteRange:
        return count / 349 - (1 / 349)
    elif count in redRange:
        return (count - 354) / 349 - (1 / 349)
    elif count in darkRedRange:
        return (count - 709) / 349 - (1 / 349)
    elif count in glowingRedRange:
        return (count - 1063) / 349 - (1 / 349)
    elif count in mirroredRange:
        return (count - 1416) / 349 - (1 / 349)
    else:
        return 0


while robot.step(timeStep) != -1:

    # always drive forward
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)

    count += 1

    distance = calculate_travel_distance(count)

    print("distance", distance)
    print(laserDistanceSensor.getValue())
    print(infraredDistanceSensor.getValue())

    if count in whiteRange:
        laser_sensor_white.append(laserDistanceSensor.getValue())
        infrared_sensor_white.append(infraredDistanceSensor.getValue())
        actual_value_white.append(distance)
    elif count in redRange:
        laser_sensor_red.append(laserDistanceSensor.getValue())
        infrared_sensor_red.append(infraredDistanceSensor.getValue())
        actual_value_red.append(distance)
    elif count in darkRedRange:
        laser_sensor_darkred.append(laserDistanceSensor.getValue())
        infrared_sensor_darkred.append(infraredDistanceSensor.getValue())
        actual_value_dark_red.append(distance)
    elif count in glowingRedRange:
        laser_sensor_glowing_red.append(laserDistanceSensor.getValue())
        infrared_sensor_glowing_red.append(infraredDistanceSensor.getValue())
        actual_value_glowing_red.append(distance)
    elif count in mirroredRange:
        laser_sensor_mirror.append(laserDistanceSensor.getValue())
        infrared_sensor_mirror.append(infraredDistanceSensor.getValue())
        actual_value_mirror.append(distance)

    if count >= 1766:
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
        break

rows = zip(laser_sensor_white, infrared_sensor_white, actual_value_white, laser_sensor_red, infrared_sensor_red,
           actual_value_red, laser_sensor_darkred, infrared_sensor_darkred, actual_value_dark_red,
           laser_sensor_glowing_red, infrared_sensor_glowing_red, actual_value_glowing_red, laser_sensor_mirror,
           infrared_sensor_mirror, actual_value_mirror)

with open("../../results/proximity.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(
        ["laser_white", "infrared_white", "actual_white", "laser_red", "infrared_red", "actual_red", "laser_dark_red",
         "infrared_dark_red", "actual_dark_red", "laser_glowing_red", "infrared_glowing_red", "actual_glowing_red",
         "laser_mirror",
         "infrared_mirror",
         "actual_mirror"])
    for row in rows:
        writer.writerow(row)
