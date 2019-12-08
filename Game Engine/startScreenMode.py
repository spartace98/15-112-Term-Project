# this is the start screen scipt
# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# i do not own the keyboard, camera or background pictures
# they are taken from
# https://www.cleanpng.com/png-computer-keyboard-cartoon-cartoon-keyboard-320938/ (keyboard)
# https://www.kissclipart.com/kamera-clipart-camera-clip-art-abaqws/ (camera)
# https://pngtree.com/freebackground/car-cartoon-background-driving-on-city-road_974628.html (background)

# future work:
# could implement caching of images

from cmu_112_graphics import *
from tkinter import *
import random
import os

# START SCREEN MODE
class StartMode(Mode):
    def appStarted(mode):
        mode.app.lastMode = mode.app.startMode
        parentDir = os.path.abspath("..")
        img_dir = os.path.join(parentDir, "Pictures/startScreen.jpg")
        mode.background = mode.loadImage(img_dir)
        width, height = mode.background.size
        # print(width, height)
        mode.background = mode.scaleImage(mode.background, mode.height/height)
        mode.time = 0
        mode.displayTitle = False
        mode.textCX = mode.width
        mode.textCY = -mode.height//3
        mode.text = ""
        mode.boxColor = ""
        mode.initOptions()
        mode.size = 0

    def initOptions(mode):
        mode.showOptions = False
        mode.buttonWidth = 200
        mode.buttonHeight = 200
        mode.cx = mode.width//2
        # button 1
        mode.leftCx = mode.width//2 - 200
        # button 2
        mode.rightCx = mode.width//2 + 200
        # common cy
        mode.cy = mode.height//2 + 100
        parentDir = os.path.abspath("..")
        # LOADING IN DESIGN IMAGES
        img_dir = os.path.join(parentDir, "Pictures/webcam.png")
        mode.webcam = mode.scaleImage(mode.loadImage(img_dir), 1/2)
        img_dir = os.path.join(parentDir, "Pictures/keyboard.png")
        mode.keyboard = mode.scaleImage(mode.loadImage(img_dir), 1/2)
        img_dir = os.path.join(parentDir, "Pictures/car1.png")
        mode.defaultCar = mode.loadImage(img_dir)
        img_dir = os.path.join(parentDir, "Pictures/palette.png")
        mode.palette = mode.scaleImage(mode.loadImage(img_dir), 1/3)
        mode.showPlayType = False
        mode.showDesignType = False

    def mousePressed(mode, event):
        # showing option screen pops up
        if mode.showOptions:
            x0, x1 = mode.leftCx - mode.buttonWidth//2, mode.leftCx + mode.buttonWidth//2
            y0, y1 = mode.cy - mode.buttonHeight//2, mode.cy + mode.buttonHeight//2
            if mode.showPlayType:
                # button 1 (with Camera)
                if x0 < event.x < x1 and y0 < event.y < y1:
                    # update the high function variable
                    mode.app.onCam = True
                    # change the active mode
                    mode.app.setActiveMode(mode.app.calibrationMode)
                    mode.showPlayType = False
                    mode.showDesignType = True
                x0, x1 = mode.rightCx - mode.buttonWidth//2, mode.rightCx + mode.buttonWidth//2
                # button 2 (without Camera)
                if x0 < event.x < x1 and y0 < event.y < y1:
                    mode.app.onCam = False
                    # change the active mode
                    mode.showPlayType = False
                    mode.showDesignType = True

            elif mode.showDesignType:
                # button 1 (with design)
                if x0 < event.x < x1 and y0 < event.y < y1:
                    # update the high function variable
                    mode.app.designCar = True
                    # change the active mode
                    mode.app.setActiveMode(mode.app.designMode)
                    mode.showDesignType = False
                x0, x1 = mode.rightCx - mode.buttonWidth//2, mode.rightCx + mode.buttonWidth//2
                # button 2 (without design)
                if x0 < event.x < x1 and y0 < event.y < y1:
                    mode.app.designCar = False
                    # change the active mode
                    mode.app.setActiveMode(mode.app.gameMode)
                    mode.showDesignType = False

    def keyPressed(mode, event):
        if event.key == "h":
            mode.app.setActiveMode(mode.app.helpMode)
            # restart the help mode instructions every time it is loaded
            mode.app.helpMode.appStarted()
        elif event.key == "Space":
            mode.app.setActiveMode(mode.app.scoresMode)

    def timerFired(mode):
        mode.time += mode.timerDelay
        if mode.textCX > mode.width//2:
            mode.size += 10
            mode.textCX -= 40

        if mode.showOptions == False and mode.time > 3000:
            mode.showOptions = True
            mode.showPlayType = True

        seconds = mode.time//1000
        if seconds%2 == 0:
            mode.boxColor = 'green'
        else:
            mode.boxColor = 'orange'

    # draw the key or open cv game optionsc
    def drawKeyPlayButton(mode, canvas):
        cx, cy = mode.width//2, mode.height//2
        cx1, cx2 = cx - mode.width//4, cx + mode.width//4
        x0, x1 = cx1 - 50, cx1 + 50
        y0, y1 = cy - 50, cy + 50
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'red')
        canvas.create_text(cx1, cy, text = "Key Presses")

    def redrawAll(mode, canvas):
        cx, cy = mode.width//2, mode.height//2
        # first draw the background
        canvas.create_image(cx, cy, image = ImageTk.PhotoImage(mode.background))
        length = mode.width*0.75
        width = mode.height//4
        # display the game intro
        if mode.showOptions == False:
            x0, x1 = mode.textCX - length//2, mode.textCX + length//2 
            y0, y1 = mode.textCY - width//2, mode.textCY + width//2
            canvas.create_rectangle(x0, y0, x1, y1, fill = mode.boxColor, outline = mode.boxColor)
            text = "     Welcome to \n Arcade Driver"
            font = f"Phosphate {mode.size} italic"
            # canvas.create_image(mode.textCX, mode.height//2, image=ImageTk.PhotoImage(mode.startingCar))
            canvas.create_text(mode.width//2, mode.height//2 - 100, text = text, fill = 'deeppink', font = font)
        else:
            canvas.create_text(mode.cx, mode.cy - 200, text = "CHOOSE YOUR\n  ADVENTURE!", font = "Phosphate 100 bold", fill = "royalblue3")

            if mode.showPlayType:
                # button 1
                canvas.create_image(mode.leftCx, mode.cy, image=ImageTk.PhotoImage(mode.webcam))
                canvas.create_text(mode.leftCx, mode.cy, text = "Camera On!", fill = 'cyan', font = "Phosphate 40")
                
                # button 2
                canvas.create_image(mode.rightCx, mode.cy, image=ImageTk.PhotoImage(mode.keyboard))
                canvas.create_text(mode.rightCx, mode.cy, text = "With Keys!", fill = 'maroon1', font = "Phosphate 40")
            elif mode.showDesignType:
                # insert the design box here
                canvas.create_image(mode.leftCx, mode.cy, image=ImageTk.PhotoImage(mode.palette))
                canvas.create_text(mode.leftCx, mode.cy, text = "Design your own!", fill = 'cyan', font = "Phosphate 40")

                canvas.create_image(mode.rightCx, mode.cy, image=ImageTk.PhotoImage(mode.defaultCar))
                canvas.create_text(mode.rightCx, mode.cy, text = "Default Car!", fill = 'maroon1', font = "Phosphate 40")

            # inform the reader of the existence of help mode
            cx, cy = mode.cx, mode.cy + 150
            canvas.create_rectangle(cx - 125, cy - 25, cx + 125, cy + 25, fill = "seagreen1", outline = "seagreen1")
            canvas.create_text(cx, cy, text = "Press H for help!", font = "Phosphate 30", fill = "royalblue1")



