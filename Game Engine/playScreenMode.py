# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# THE CAR AND SHRUB IMAGES DO NOT BELONG TO ME
# THEY ARE CITED FROM THE FOLLOWING WEBSITES
# https://www.freepik.com/free-vector/top-view-six-different-cars-with-reflecting-windshields_1349964.htm (CARS)
# https://myrealdomain.com/explore/cartoon-bushes-clipart.html (SHRUB)
# this script only handles the play game screen mode

from cmu_112_graphics import *
from tkinter import *
import random
import os
from randomMapGeneratorv2 import RandomRoadGenerator, StraightPiece, RightTurnPiece, StartingPiece, EndPiece
import math
from randomCarsGenerator import RandomCarsGenerator, Car
from aprilTagDetectorv2 import AprilTagDetector
import cv2

# GAME SCREEN MODE
class GameMode(Mode):
    def appStarted(mode):
        # ModalApp.width, ModalApp.height = 500, 800s
        # mode.width, mode.height = 500, 800
        # standard car specs
        mode.time = 0
        mode.countDown = 3
        # GENERATING ROADS AND CARS
        mode.initRoadsandCars()
        mode.initCrashImage()
        mode.playerX, mode.playerY = mode.width//2, mode.height-80
        mode.playerSpeed = 20
        # current piece of the player
        mode.currentPiece = None
        mode.gameStarted = False
        mode.dx = 0
        mode.dy = mode.playerSpeed
        mode.angle = 0
        mode.prevAngle = 0
        mode.anglesZ = [0, 0, 0]
        mode.yDistanceTravelled = 0
        mode.collisionTimer = 0
        mode.carCollide = None
        mode.prevCarCollided = None
        mode.onCam = mode.app.onCam
        mode.app.lastMode = mode.app.gameMode
        if mode.onCam:
            mode.cam = cv2.VideoCapture(0)

    def initRoadsandCars(mode):
        # GENERATING SHRUBS
        parentDir = os.path.abspath("..")
        img_dir = os.path.join(parentDir, "Pictures/shrub.png")
        mode.shurbImg = mode.scaleImage(mode.loadImage(img_dir), 1/3)
        # GENERATING RANDOM ROAD
        numRoads = 35
        roadGenerator = RandomRoadGenerator(mode.width, mode.height, mode.shurbImg, numRoads)
        mode.roads = roadGenerator.getRandomRoad()
        mode.roadDistance = roadGenerator.getTotalDistance()
        mode.shrubs = roadGenerator.getShrubs()
        # GENERATING CARS
        # CHECK IF THE PLAYER CREATED HIS CUSTOM CAR
        if mode.app.designCar == False:
            # initialise the player car
            img_dir = os.path.join(parentDir, "Pictures/car1.png")
            mode.playerCarImg = mode.loadImage(img_dir)
            # mode.playerCarImg = mode.scaleImage(mode.playerCarImg, 1/2)
            mode.carWidth, mode.carLength = mode.playerCarImg.size[0], mode.playerCarImg.size[1]
            mode.playerCar = Car(mode.width//2, mode.height*0.8, mode.carLength, mode.carWidth, 'blue', image = mode.playerCarImg, cache = False)
            # GENERATING OTHER CARS
            mode.otherCarsImgs = []
            # creating addresses to the other cars
            carsNames = ["car2.png", "car3.png", "car4.png", "car5.png", "car6.png"]
            for img_dir in carsNames:
                img_dir = os.path.join(parentDir, "Pictures/" + img_dir)
                mode.otherCar = mode.loadImage(img_dir)
                # mode.otherCar = mode.scaleImage(mode.otherCar, 1/2)
                mode.otherCarsImgs.append(mode.otherCar)
        # if the player designed his own car
        else:
            img_dir = os.path.join(parentDir, "Pictures/customPlayerCar.png")
            mode.playerCarImg = mode.loadImage(img_dir)
            mode.carWidth, mode.carLength = mode.playerCarImg.size[0], mode.playerCarImg.size[1]
            mode.playerCar = Car(mode.width//2, mode.height*0.8, mode.carLength, mode.carWidth, 'blue', image = mode.playerCarImg, cache = False)
            # GENERATING OTHER CARS
            mode.otherCarsImgs = []
            # creating addresses to the other cars
            carsNames = ["customCar_0.png", "customCar_1.png", "customCar_2.png", "customCar_3.png", "customCar_4.png"]
            for img_dir in carsNames:
                img_dir = os.path.join(parentDir, "Pictures/" + img_dir)
                mode.otherCar = mode.loadImage(img_dir)
                # mode.otherCar = mode.scaleImage(mode.otherCar, 1/2)
                mode.otherCarsImgs.append(mode.otherCar)
        mode.cars = RandomCarsGenerator(numRoads, mode.roadDistance, mode.roads, mode.height, mode.carLength, mode.carWidth, mode.otherCarsImgs).generateCars()
        mode.backgroundColor = 'forest green'
        mode.roadColor = 'gray25'
        mode.lapsLeftDisplay = None
        mode.sideTimer = 0
        mode.fuelBar = 100
        mode.refuelling = False
        print("Road Distance:", mode.roadDistance)

    def keyPressed(mode, event):
        if not mode.onCam:
            # moving the pieces
            # can only move the car if the game has started
            if mode.carCollide == None:
                if event.key == "Left":
                    mode.angle = math.pi//3
                    mode.dx = mode.playerSpeed * math.sin(mode.angle)
                    mode.dy = mode.playerSpeed * math.cos(mode.angle)
                elif event.key == "Right":
                    mode.angle = -(math.pi//3)
                    mode.dx = (mode.playerSpeed * math.sin(mode.angle))
                    mode.dy = mode.playerSpeed * math.cos(mode.angle)
                elif event.key == "Up":
                    if int(mode.playerSpeed) <= 0:
                        mode.playerSpeed += 5
                    mode.playerSpeed *= 1.1
                    if mode.playerSpeed >= 180:
                        mode.playerSpeed = 180
                elif event.key == "Down":
                    # constant backing speed
                    if int(mode.playerSpeed) <= 0:
                        mode.playerSpeed = -10
                    else:
                        mode.playerSpeed *= 0.9
                else:
                    mode.dx = 0
                    mode.dy = mode.playerSpeed
            else:
                pass
        # refuelling, which takes time
        if event.key == "Space":
            mode.refuelling = True
            mode.fuelBar += 5
            if mode.fuelBar > 100:
                mode.fuelBar = 100
                mode.refuelling = False

        # moves to the help page
        if event.key == "h":
            mode.app.setActiveMode(mode.app.helpMode)
            # restart the help mode instructions every time it is loaded
            mode.app.helpMode.appStarted()

    def initCrashImage(mode):
        parentDir = os.path.abspath("..")
        img_dir = os.path.join(parentDir, "Pictures/pow.png")
        mode.pow = mode.loadImage(img_dir)
        mode.pow = mode.scaleImage(mode.pow, 1/2)

    def keyReleased(mode, event):
        if mode.carCollide == None:
            mode.dx = 0
            mode.dy = mode.playerSpeed
            mode.angle = 0

    def cameraRotations(mode):
        # initialise the detector
        ret, frame = mode.cam.read()
        ATD = AprilTagDetector(frame)
        angles = ATD.getAngles()
        # set the mode angle to the angle of rotation
        if angles != None: 
            angleX, angleY, angleZ = angles[0]
            # ensuring stability in the rotation, assumes that the player cannot turn fast enough
            # print(angleZ)
            if abs(mode.prevAngle) - abs(angleZ) < 45:
                # first get the angleZ, aka the left right angle
                # convert to degrees
                angleZ = (angleZ / 180) * math.pi
                # the mode angle is only concerned with angleZ
                mode.angle = angleZ
                mode.dx = mode.playerSpeed * math.sin(angleZ)
                # tilt forward and backwards
                # print(angleX)
                if angleX > 5:
                    mode.playerSpeed += 5
                elif angleX < -100:
                    mode.playerSpeed -= 5
                mode.prevAngle = angleZ
            # else:
            #     mode.prevAngle = angleZ
            # angleZ = mode.getStableAngleZ(angleZ)
            # print(angleZ)
            # # the mode angle is only concerned with angleZ
            # mode.angle = angleZ
            # mode.dx = mode.playerSpeed * math.sin(angleZ)
            # # tilt forward and backwards
            # # print(angleX)
            # if angleX > 5:
            #     mode.playerSpeed += 5
            # elif angleX < -100:
            #     mode.playerSpeed -= 5

        mode.dy = mode.playerSpeed * math.cos(mode.angle)

    # ensuring camera stability, get the average of the past 3 angleZ
    def getStableAngleZ(mode, angleZ):
        # append this angle
        mode.anglesZ.append(angleZ)
        # remove the earliest angle
        mode.anglesZ.pop(0)
        return sum(mode.anglesZ)/3

    # only timer fired does the moving
    def timerFired(mode):
        if mode.gameStarted == False:
            mode.time += mode.timerDelay
            mode.countDown = 3 - mode.time//1000
            if mode.time > 3000:
                mode.gameStarted = True
                mode.time = 0
        else:
            mode.time += mode.timerDelay
            # if the fuel bar is non 0 and is not currently refuelling
            if mode.fuelBar > 0 and mode.refuelling == False:
                mode.fuelBar -= 0.1
            # if the player is not colliding with any cars
            if mode.carCollide == None:
                # if there is no more fuel
                # need to press Space Bar to refuel
                if mode.fuelBar <= 0 or mode.refuelling:
                    return

                if mode.onCam:
                    mode.cameraRotations()
            
                # if the camera is not on, the player horizontal movement is controlled by the keypresses
                else:
                    mode.dx = mode.playerSpeed * math.sin(mode.angle)
                    mode.dy = mode.playerSpeed * math.cos(mode.angle)

                mode.yDistanceTravelled += mode.dy
                for roadPiece in mode.roads:
                    # detects the current piece within of the each specific piece range
                    if roadPiece.cy - roadPiece.roadHeight < mode.playerY < roadPiece.cy:
                        mode.currentPiece = roadPiece
                    # move each piece based on the speed
                    roadPiece.cy += mode.dy
                    # print(mode.dy, mode.playerSpeed)
                    roadPiece.cx += mode.dx

                # translate the positions of the car also
                # but each of the enemy cars also move randomly
                # if the car y position is greater than the total road distance, remove the car
                i = 0
                while i < len(mode.cars):
                    car = mode.cars[i]
                    car.cx += mode.dx
                    car.cy += mode.dy
                    try:
                        car.steerCar(mode.roads)
                        i += 1
                    # if the car cannot be steered, it means it has travelled out of max distance
                    # so remove it
                    except:
                        print('Removing car', car)
                        print("Car Position:", car.cy)
                        print("Distance Travelled", mode.yDistanceTravelled)
                        mode.cars.remove(car)
                # translate the position of the shrubs
                for shrub in mode.shrubs:
                    shrub.cx += mode.dx
                    shrub.cy += mode.dy

            # if the car is colliding with other cars, 
            # deplete the fuel by 5
            else:
                mode.dy = mode.playerSpeed
                mode.dx = 0
                mode.fuelBar -= 0.5

            mode.checkCollision()

            # game has completed, change to the game over mode
            if mode.yDistanceTravelled > abs(mode.roadDistance):
                mode.dy = 0
                # save the time in seconds
                mode.app.finalTime = mode.time//1000
                mode.app.setActiveMode(mode.app.gameOverMode)

    def checkCollision(mode):
        # constantly detect if the player is out of bounds
        if mode.currentPiece != None:
            if mode.currentPiece.detectOutOfBounds(mode.playerX, mode.playerY):
                if abs(mode.playerSpeed) > 5:
                    mode.playerSpeed *= 0.9

        # check collisions of the player car with any of the other cars
        for car in mode.cars:
            # that are within the canvas screen
            if 0 < car.cy < mode.height:
                # this is the collision method from the Car class
                if Car.checkCollision(car, mode.playerCar) and car != mode.prevCarCollided:
                    mode.carCollide = car
                    mode.prevCarCollided = None
                    mode.playerSpeed = 5
                    # dont have to check other cars if there is collision
                    break

        # start the collision delay timer
        if mode.carCollide != None:
            mode.collisionTimer += mode.timerDelay
            # if the collision delay is greater than 1s, reset the timer
            if mode.collisionTimer > 1000:
                mode.collisionTimer = 0
                mode.prevCarCollided = mode.carCollide
                mode.carCollide = None
                mode.angle = 0

    def drawSpeedometer(mode, canvas):
        radius = 100
        # speedometer is a half arc, with a line indicating the speed
        cx, cy = mode.width - 1.6*radius, radius
        width, length = mode.width//5, mode.height//8
        x0, x1 = cx - width//2, cx + width//2
        y0, y1 = cy - length//2, cy + length//2
        # canvas.create_rectangle(x0, y0, x1, y1, fill = 'orange', outline = 'orange')
        # create the semicircle
        cy += radius//3
        x0, x1 = cx - radius, cx + radius
        y0, y1 = cy - radius, cy + radius
        canvas.create_arc(x0, y0, x1, y1, extent = 180, fill = 'hotpink1', outline = 'gold', width = 3)
        canvas.create_text(cx, cy, fill = 'goldenrod1', font = "Phosphate 50 italic", text = "SPEEDOMETER")
        angle = (mode.dy / 180) * math.pi
        needleLength = radius - 10
        xEnd = cx - needleLength*math.cos(angle)
        yEnd = cy - abs(needleLength*math.sin(angle))
        canvas.create_line(cx, cy, xEnd, yEnd, fill = 'white', width = 5)
        speed = f"{round(mode.dy)} km/h"
        cy -= 50
        canvas.create_text(cx, cy, text = speed, font = "Arial 20 bold", fill = 'white')

    def drawFuelBar(mode, canvas):
        fuelLeft = mode.fuelBar
        percentageFuelLeft = mode.fuelBar/100
        barLength, barWidth = 300, 50
        cx, cy = mode.width - 75, mode.height//2 + 150
        x0, x1 = cx - barWidth//2, cx + barWidth//2
        y0, y1 = cy - barLength//2, cy + barLength//2
        canvas.create_rectangle(x0, y0, x1, y1, fill = "gray39")
        y0 = y1 - percentageFuelLeft*barLength
        color = 'springgreen'
        if 0.60 < percentageFuelLeft < 0.80:
            color = "yellow"
        elif 0.40 < percentageFuelLeft < 0.60:
            color = "orange"
        elif percentageFuelLeft < 0.40:
            color = "red"
        canvas.create_rectangle(x0, y0, x1, y1, fill = color)
        canvas.create_text(cx, y1 + 20, text = "FUEL LEFT", font = "Phosphate 30 italic", fill = 'tomato')

    def drawTimer(mode, canvas):
        if mode.gameStarted == 0:
            minutes = 0
            seconds = 0
        else:
            timePassedInSeconds = (mode.time//1000)
            minutes = timePassedInSeconds//60
            seconds = timePassedInSeconds%60
        if seconds < 10:
            seconds = f"0{seconds}"
        time = f"{minutes}:{seconds}"
        cx = mode.width//2
        cy = mode.height//8 + 25
        boxLength, boxWidth = 150, 50
        x0, x1 = cx - boxLength//2, cx + boxLength//2
        y0, y1 = cy - boxWidth//2, cy + boxWidth//2
        # canvas.create_text()
        canvas.create_rectangle(x0, y0, x1, y1, fill = "royalblue4", outline = 'blue')
        canvas.create_text(cx, cy, text = time, fill = "white", font = "Arial 20 bold")
        # drawign the label
        canvas.create_text(cx, cy - 50, text = "TIMER", fill = 'maroon1', font = "Phosphate 50 italic")

    def drawDistanceTravelled(mode, canvas):
        distanceLeft = int(mode.roadDistance - abs(mode.yDistanceTravelled))
        if distanceLeft < 0:
            distanceLeft = 0
        # if there is only 2km left 
        elif distanceLeft < 2000:
            mode.lapsLeftDisplay = 1000
        # if there is only 5km left 
        elif distanceLeft < 5000:
            # display on screen temporarily
            mode.lapsLeftDisplay = 5000
        cx = mode.width//5
        cy = mode.height//8 + 25
        # drawing the distance left box
        boxLength, boxWidth = 250, 50
        x0, x1 = cx - boxLength//2, cx + boxLength//2
        y0, y1 = cy - boxWidth//2, cy + boxWidth//2
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'deeppink1', outline = 'deeppink1')
        percentageComplete = mode.yDistanceTravelled/abs(mode.roadDistance)
        x1 = percentageComplete*boxLength + x0
        canvas.create_rectangle(x0, y0, x1, y1-1, fill = 'deepskyblue', outline = 'deepskyblue')

        if mode.yDistanceTravelled > 10000:
            # draw the distance more to cover text
            dTravlledCX = (x0+x1)*0.5
            text = f"{int(mode.yDistanceTravelled)}m"
            canvas.create_text(dTravlledCX, cy, text = text, fill = "white", font = "Arial 20 bold")
        else:
            # draw the distance left text
            dLeftCX = (x1 + cx + boxLength//2)*0.5
            text = f"{distanceLeft}m"
            canvas.create_text(dLeftCX, cy, text = text, fill = "white", font = "Arial 20 bold")

        # drawing the label
        canvas.create_text(cx, cy - 50, text = "ODOMETER", fill = "cyan2", font = "Phosphate 50 italic")

    def drawCrash(mode, canvas):
        cx, cy = mode.playerCar.cx, mode.playerCar.cy
        canvas.create_image(cx, cy, image = ImageTk.PhotoImage(mode.pow))

    def redrawAll(mode, canvas):
        cx, cy = mode.width//2, mode.height//2
        canvas.create_text(cx, cy, text = "gamescreen")
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = mode.backgroundColor)
        cx, cy = mode.width//2, mode.height//2
        # first draw the background
        for roadPiece in mode.roads:
            # only drawing the parts of the road that are within the canvas
            if 0 <= roadPiece.cy <= mode.height or -mode.height <= (roadPiece.cy - roadPiece.roadHeight) <= mode.height:
                if isinstance(roadPiece, StartingPiece) or isinstance(roadPiece, EndPiece):
                    p1 = roadPiece.getStraightPiece()
                    canvas.create_rectangle(p1, fill = mode.roadColor, outline = mode.roadColor)
                    x0, y0, x1, y1 = roadPiece.getRibbonBox()
                    ribbonLength = (x1-x0)/10
                    ribbonHeight = (y1-y0)/5
                    for i in range(10):
                        for j in range(5):
                            if (i+j)%2 == 0:
                                color = 'white'
                            else:
                                color = 'black'
                            x2, x3 = x0 + i * ribbonLength, x0 + (i+1) * ribbonLength
                            y2, y3 = y1 - j * ribbonHeight, y1 - (j+1) * ribbonHeight
                            canvas.create_rectangle(x2, y2, x3, y3, fill = color, outline = color)
                elif isinstance(roadPiece, StraightPiece):
                    p1 = roadPiece.getStraightPiece()
                    canvas.create_rectangle(p1, fill = mode.roadColor, outline = mode.roadColor)

                elif isinstance(roadPiece, RightTurnPiece):
                    p1, p2, p3, p4 = roadPiece.getRightTurnPiece()
                    canvas.create_arc(p2, fill = mode.roadColor, start = 90, outline = mode.roadColor)
                    canvas.create_arc(p1, fill = mode.backgroundColor, start = 90, outline = mode.backgroundColor)
                    canvas.create_arc(p4, fill = mode.roadColor, start = 270, outline = mode.roadColor)
                    canvas.create_arc(p3, fill = mode.backgroundColor, start = 270, outline = mode.backgroundColor)

                else:
                    p1, p2, p3, p4 = roadPiece.getLeftTurnPiece()
                    canvas.create_arc(p2, fill = mode.roadColor, start = 0, outline = mode.roadColor)
                    canvas.create_arc(p1, fill = mode.backgroundColor, start = 0, outline = mode.backgroundColor)
                    canvas.create_arc(p4, fill = mode.roadColor, start = 180, outline = mode.roadColor)
                    canvas.create_arc(p3, fill = mode.backgroundColor, start = 180, outline = mode.backgroundColor)

        for shrub in mode.shrubs:
            if 0 < shrub.cy < mode.height:
                shrub.drawShrub(canvas)

        # drawing all the cars
        for car in mode.cars:
            # only drawing the cars that are visible within the canvas
            if 0 < car.cy < mode.height:
                car.drawCar(canvas)

        # drawing the player
        mode.playerCar.rotate = mode.angle
        mode.playerCar.drawCar(canvas, cache = False)

        # if the car collide, print the message out
        if mode.carCollide != None:
            mode.drawCrash(canvas)

        # draw the speedometer
        mode.drawSpeedometer(canvas)

        # drawing the countdown
        if mode.gameStarted == False:
            if mode.countDown == 0:
                text = "Go!"
            else:
                text = str(mode.countDown)
            canvas.create_text(mode.width//2, mode.height//2, fill = 'white', text = text, font = "Arial 100 bold")

        # drawing the time passed
        mode.drawTimer(canvas)
        # drawing the odometer
        mode.drawDistanceTravelled(canvas)
        # drawing the fuel bar
        mode.drawFuelBar(canvas)

        # display the distance left
        if mode.lapsLeftDisplay != None:
            cx = mode.width//2
            cy = mode.height//2
            text = f"{mode.lapsLeftDisplay}m LEFT!"
            if mode.lapsLeftDisplay == 5000:
                color = "orangered"
            else:
                color = "firebrick1"
            canvas.create_text(cx, cy, text = text, fill = color, font = "PHOSPHATE 50 italic")
            mode.sideTimer += mode.timerDelay

        # if there is no more fuel, tell the player
        if mode.fuelBar <= 0:
            canvas.create_text(mode.width//2, mode.height//2, text = "REFUEL!", font = "Phosphate 50 bold", fill = "deeppink1")



