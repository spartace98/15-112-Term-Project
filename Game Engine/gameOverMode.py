# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# I DO NOT OWN THE BACKGROUND IMAGE
# IT IS TAKEN FROM https://www.pinterest.com/pin/401946335469846161/

from cmu_112_graphics import *
from tkinter import *
import os
from highScoreMonitor import HighScore
from datetime import date

# GAME OVER MODE ALLOWS USER TO ENTER HIS NAME
class GameOverMode(Mode):
    def appStarted(mode):
        # mode.time = 0
        mode.gameOverTextX = mode.width
        mode.gameOverTextY = 0
        mode.displayGameOverText = True
        mode.name = []
        mode.sideTimer = 0
        parentDir = os.path.abspath("..")
        img_dir = os.path.join(parentDir, "Pictures/endGame.png")
        mode.background = mode.loadImage(img_dir)
        width, height = mode.background.size
        mode.background = mode.scaleImage(mode.background, mode.height/height)
        mode.app.lastMode = mode.app.gameOverMode

    def timerFired(mode):
        # mode.time += mode.timerDelay
        # print the game over screen for the first 3 seconds
        if mode.gameOverTextY < mode.height//2:
            mode.gameOverTextY += 20
        if mode.gameOverTextX > mode.width//2:
            mode.gameOverTextX -= 20
        # pauses the screen for 3s
        if mode.gameOverTextY >= mode.height//2:
            mode.sideTimer += mode.timerDelay
        if mode.sideTimer > 1000:
            mode.displayGameOverText = False

    def keyPressed(mode, event):
        # game over is the only mode you cannot access help mode
        # if event.key == "h":
        #     mode.app.setActiveMode(mode.app.helpMode)
        if mode.displayGameOverText == False:
            bannedKeys = ["Space", "Delete", "Up", "Down", "Left", "Right", "Enter"]
            # cut the characters after 10
            if len(mode.name) > 10 and event.key != "Delete":
                return
            elif event.key == "Delete" and mode.name != []:
                mode.name.pop()
            elif event.key not in bannedKeys:
                mode.name.append(event.key)
            elif event.key == "Space":
                mode.name.append(" ")
            elif event.key == "Enter":
                # save the name and score to the csv file
                scores = HighScore()
                name = "".join(mode.name)
                today = date.today()
                today = today.strftime("%b-%d-%Y")
                scores.addNewEntry(name, mode.app.finalTime, today)
                scores.saveResults()
                mode.app.setActiveMode(mode.app.scoresMode)
                # reset to display the new results
                mode.app.scoresMode.appStarted()

    # from 112 course website "https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html"
    def getCachedPhotoImage(mode, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def redrawAll(mode, canvas):
        # canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'black')
        cx, cy = mode.width//2, mode.height//2
        # first draw the background
        canvas.create_image(cx, cy, image = ImageTk.PhotoImage(mode.background))
        if mode.displayGameOverText:
            canvas.create_text(mode.width//2, mode.gameOverTextY, text = "GAME OVER", fill = 'blue', font = "Phosphate 80")
            canvas.create_text(mode.gameOverTextX, mode.height//2, text = "GAME OVER", fill = 'green', font = "Phosphate 80")
            canvas.create_text(mode.width - mode.gameOverTextX, mode.height//2, text = "GAME OVER", fill = 'red', font = "Phosphate 80")
            canvas.create_text(mode.width//2, mode.height - mode.gameOverTextY, text = "GAME OVER", fill = 'yellow', font = "Phosphate 80")
        else:
            canvas.create_text(mode.width//2, mode.height//2 - 100, text = "Enter your name!", font = "Phosphate 80 bold", fill = "aquamarine")
            # allow the user to type his name
            # create a white box
            boxLength, boxWidth = 200, 50
            x0, x1 = mode.width//2 - boxLength//2, mode.width//2 + boxLength//2
            y0, y1 = mode.height//2 - boxWidth//2, mode.height//2 + boxWidth//2
            canvas.create_rectangle(x0, y0, x1, y1, outline = 'black', fill = "white")
            text = "".join(mode.name)
            canvas.create_text(mode.width//2, mode.height//2, text = text, fill = 'violetred3', font = "Phosphate 20")
            # insert the picture (if any) at the top left
            if mode.app.selfie != None:
                canvas.create_image(mode.width//2, 3*mode.height//4, image = ImageTk.PhotoImage(mode.app.selfie))



