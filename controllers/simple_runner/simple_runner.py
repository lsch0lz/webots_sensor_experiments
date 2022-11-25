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
outerLeftSensor = robot.getDevice("prox.horizontal.0")
centralLeftSensor = robot.getDevice("prox.horizontal.1")
centralSensor = robot.getDevice("prox.horizontal.2")
centralRightSensor = robot.getDevice("prox.horizontal.3")
outerRightSensor = robot.getDevice("prox.horizontal.4")


outerLeftSensor.enable(timeStep)
centralLeftSensor.enable(timeStep)
centralSensor.enable(timeStep)
centralRightSensor.enable(timeStep)
outerRightSensor.enable(timeStep)

# ground sensors
groundLeftSensor = robot.getDevice("prox.ground.0")
groundRightSensor = robot.getDevice("prox.ground.1")

groundLeftSensor.enable(timeStep)
groundRightSensor.enable(timeStep)

# Disable motor PID
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

velocity = 0.7 * maxMotorVelocity

ground_sensor = []
central_sensor = []
outer_left_sensor = []

count = 0
while robot.step(timeStep) != -1:
    # always drive forward
    
    ground_sensor.append(groundRightSensor.getValue())
    central_sensor.append(centralSensor.getValue())
    outer_left_sensor.append(outerLeftSensor.getValue())
    
    leftMotor.setVelocity(velocity)
    rightMotor.setVelocity(velocity)
    # register black dot    
    if groundRightSensor.getValue() < 200:
        count = count + 1
    # register wall and turn right
    if centralSensor.getValue() > 0 or outerLeftSensor.getValue() > 0:
        leftMotor.setVelocity(velocity)
        rightMotor.setVelocity(-velocity*2)
    # stop condition
    if count > 200 and centralSensor.getValue() > 0:
        velocity = 0
        break
rows = zip(ground_sensor, central_sensor, outer_left_sensor)

with open("../../results/simple_runner.csv", "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
