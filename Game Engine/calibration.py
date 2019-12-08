"""
THINGS TO DO
# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
"""

# frame by frame slide the image
import numpy as np
import cv2
from aprilTagDetectorv2 import AprilTagDetector
from drawCorners import DrawCorners
from cmu_112_graphics import *
from tkinter import *
from PIL import Image

class VideoCapture(Mode):
    def appStarted(mode):
        mode.time = 0
        mode.cx, mode.cy = mode.width//2, mode.height//2
        mode.stepsCompleted = []
        # cv2.namedWindow("preview")
        mode.cap = cv2.VideoCapture(0)
        mode.displayImg = None
        # boolean to start the camera detection
        mode.startInstructions = False
        mode.sideTimer = 0
        mode.selfie = None
        mode.angleZ = 0

    def timerFired(mode):
        # first check if angle is detectable'
        if mode.startInstructions:
            angleZ = mode.getAngle()
            # next check if straight, left and right twists are detectable
            # keep the twisting threshold at 60 degrees
            if angleZ != None:
                # print(angleZ)
                mode.angleZ = angleZ
                if len(mode.stepsCompleted) == 0 and angleZ != None:
                    mode.stepsCompleted.append(1)
                elif len(mode.stepsCompleted) == 1 and -10 < angleZ < 10:
                    mode.stepsCompleted.append(1)
                elif len(mode.stepsCompleted) == 2 and 60 < angleZ < 90:
                    mode.stepsCompleted.append(1)
                    # print("YES!")
                # next check if right twist is detectable
                elif len(mode.stepsCompleted) == 3 and -90 < angleZ < -60:
                    mode.stepsCompleted.append(1)
                    # print("YES!")
                # print(mode.stepsCompleted)
        mode.time += mode.timerDelay

        # all the steps have been completed
        # tell the user the program is about to take a screenshot
        if len(mode.stepsCompleted) == 4:
            mode.sideTimer += mode.timerDelay
            if mode.sideTimer == 3000 and mode.selfie == None:
                # take a screenshot of the player and save to high level attribute
                mode.app.selfie = mode.app.getSnapshot().crop((300, 300, 1500, 1500))
                mode.app.selfie = mode.scaleImage(mode.app.selfie, 1/4)
                # change the active mode here
                mode.app.setActiveMode(mode.app.lastMode)

    def getAngle(mode):
        ret, frame = mode.cap.read()
        # INITIALISING APRIL TAG DETECTOR
        ATD = AprilTagDetector(frame)
        corners = ATD.getCorners()

        # IF THE CORNERS CAN BE DETECTED and before the selfie shot
        if corners != None and len(mode.stepsCompleted) != 4:
            angleZ = ATD.getAngles()[0][2]
            # initialise the draw corners function
            mode.displayImg = DrawCorners(corners, frame).drawCorners()
            # You may need to convert the color
            # adapted from https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format
            mode.displayImg = cv2.cvtColor(mode.displayImg, cv2.COLOR_BGR2RGB)
            mode.displayImg = Image.fromarray(mode.displayImg)

        # IF NO CORNERS ARE DETECTED
        else:
            angleZ = None
            mode.displayImg = frame
            mode.displayImg = cv2.cvtColor(mode.displayImg, cv2.COLOR_BGR2RGB)
            mode.displayImg = Image.fromarray(mode.displayImg)

        return angleZ

    def detectedAprilTag(mode, angle):
        pass

    def redrawAll(mode, canvas):
        # display starting instructions for 5 seconds
        if mode.time < 3000:
            canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "turquoise1")
            text = "         Find a position that detects\nyour april tag with green corners\n           and follow instructions\n\n               remember this position \n                 when playing game"
            canvas.create_text(mode.cx, mode.cy, text = text, font = "Phosphate 40 bold", fill = "magenta2")
        else:
            mode.startInstructions = True
            if mode.displayImg != None:
                canvas.create_image(mode.cx, mode.cy, image = ImageTk.PhotoImage(mode.displayImg))
                # if not completed
            if 150 < abs(mode.angleZ) < 210 and len(mode.stepsCompleted) != 4:
                canvas.create_text(mode.cx, mode.cy + 80, text = "You're holding it upside down!", font = "Phosphate 50 bold", fill = "red")
            # step wise display instructions
            if len(mode.stepsCompleted) == 0:
                canvas.create_text(mode.cx, mode.cy, text = "Hold up your April Tag", font = "Phosphate 50 bold", fill = "springgreen2")
            elif len(mode.stepsCompleted) == 1:
                canvas.create_text(mode.cx, mode.cy, text = "Hold April Tag Straight Up", font = "Phosphate 50 bold", fill = "springgreen2")
            elif len(mode.stepsCompleted) == 2:
                canvas.create_text(mode.cx, mode.cy, text = "Twist Left", font = "Phosphate 50 bold", fill = "springgreen2")
            elif len(mode.stepsCompleted) == 3:
                canvas.create_text(mode.cx, mode.cy, text = "Twist Right", font = "Phosphate 50 bold", fill = "springgreen2")

            # create 4 rectangular boxes
            xOffset = 50
            yOffset = 100
            for i in range(4):
                x0 = xOffset + i*50
                x1 = xOffset + (i+1)*50
                y0 = yOffset
                y1 = yOffset + 50
                canvas.create_rectangle(x0, y0, x1, y1, fill = "white")
                # if the level is completed
            for i in range(len(mode.stepsCompleted)):
                x0 = xOffset + i*50
                x1 = xOffset + (i+1)*50
                y0 = yOffset
                y1 = yOffset + 50
                canvas.create_rectangle(x0, y0, x1, y1, fill = "green")
                # draw a tick
                mode.drawTick(canvas, x0, y0, x1, y1)

            # draw the title
            canvas.create_text(xOffset+100, yOffset, text = "Calibration Steps", font = "Phosphate 30 bold", fill = "hotpink")

            # prepare the user for the screenshot
            if len(mode.stepsCompleted) == 4:
                timeLeft = 3 - mode.sideTimer/1000
                if timeLeft >= 1:
                    canvas.create_text(mode.cx, mode.cy, text = f"{round(timeLeft)}s to photo\nSMILE!", font = "Phosphate 30 bold", fill = "cyan")

    def drawTick(mode, canvas, x0, y0, x1, y1):
        # draw a tick here
        x2 = 0.25*(x1-x0) + x0
        y2 = 0.50*(y1-y0) + y0
        x3 = 0.50*(x1-x0) + x0
        y3 = 0.75*(y1-y0) + y0
        canvas.create_line(x2, y2, x3, y3, fill = "black", width = 2)
        x4 = 0.75*(x1-x0) + x0
        y4 = 0.25*(y1-y0) + y0
        canvas.create_line(x3, y3, x4, y4, fill = "black", width = 2)

# class MyModalApp(ModalApp):
#     def appStarted(app):
#         app.videoMode = VideoCapture()
#         app.setActiveMode(app.videoMode)

# app = MyModalApp(width=800, height=800)

# app = MyModalApp(width=600, height=600)

# cv2.namedWindow("preview")
# cap = cv2.VideoCapture(0)

# shoot = False

# while(True):
#     ret, frame = cap.read()
#     # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # INITIALISING APRIL TAG DETECTOR
#     ATD = AprilTagDetector(frame)
#     corners = ATD.getCorners()
#     # print(corners)

#     # IF THE CORNERS CAN BE DETECTED
#     if corners != None:
#     	angles = ATD.getAngles()
#     	print(angles[0][2])
#     	if abs(angles[0][2]) > 45:
#     		shoot = True
#     	else:
#     		shoot = False
#     	# initialise the draw corners function
#     	img_corners = DrawCorners(corners, frame).drawCorners()
#     	cv2.imshow('frame',img_corners)

#     # IF NO CORNERS ARE DETECTED
#     else:
#     	shoot = False
#     	cv2.imshow('frame', frame)

#     print(shoot)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# #do some ops
# cap.release()
# cv2.imshow("output", output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


