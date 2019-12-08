# this is the help mode
# this help mode will be completely animated
# with credit scenes, every new sentence will be animated

# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# I do not own the helpmode background. it is obtained from the following website
# colourbox.com/vector/cartoon-night-city-vector-10366806
# I do not own the police and wooden board image 
# https://imgbin.com/png/q8Q7vVad/cartoon-police-officer-stock-illustration-png (police)
# https://pixabay.com/vectors/wood-board-wooden-plank-panel-601830/ (wooden board)

from cmu_112_graphics import *
from tkinter import *

class HelpMode(Mode):
    def appStarted(mode):
        mode.time = 0
        mode.texts = ["Use Arrow Keys\nin keyboard mode",
                      "    In Camera Mode\n    Hold up your    \n        April Tag      \n   Steering Wheel", 
                      "Twist the wheel\n  left and right\nto steer the Car", 
                      "Twist wheel forward\n     and backwards\n   to control speed",
                      "Travelling off\n     the road\nwill decrease\n  your speed", 
                      "  Colliding with\n      other cars\n      will stun\nand deplete fuel",
                      "Press and Hold\n Space to refuel",
                      "Complete the track\nas fast as possible!", 
                      "Have Fun!"]
        mode.displayText = None
        mode.index = 0
        mode.switchTime = 2000
        mode.textColors = ['deeppink2', 'yellow2', 'orange', 'lawngreen']*3
        mode.backgroundColors = ['lightgreen', 'deepskyblue', 'purple', 'deeppink2']*3
        parentDir = os.path.abspath("..")
        img_dir = os.path.join(parentDir, "Pictures/helpModeBackground2.jpg")
        mode.background = mode.scaleImage(mode.loadImage(img_dir), 1.5)
        img_dir = os.path.join(parentDir, "Pictures/police.png")
        mode.police = mode.scaleImage(mode.loadImage(img_dir), 0.6)
        img_dir = os.path.join(parentDir, "Pictures/woodenSign.png")
        mode.woodenSign = mode.scaleImage(mode.loadImage(img_dir), 0.50)

    def keyPressed(mode, event):
        if event.key == "Left":
            mode.index -= 1
            mode.time = mode.index*mode.switchTime
        elif event.key == "Right":
            mode.index += 1
            mode.time = mode.index*mode.switchTime
        if event.key == "h":
            # set the active mode back to the previous mode (access through top level class)
            mode.app.setActiveMode(mode.app.lastMode)

    def timerFired(mode):
        mode.time += mode.timerDelay
        mode.index = (mode.time//mode.switchTime)%len(mode.texts)
        mode.displayText = mode.texts[mode.index]

    def redrawAll(mode, canvas):
        # color = mode.backgroundColors[mode.index]
        # canvas.create_rectangle(0, 0, mode.width, mode.height, fill = "lightblue")
        canvas.create_image(mode.width//2, mode.height//2, image=ImageTk.PhotoImage(mode.background))
        # color = mode.textColors[mode.index]
        # canvas.create_text(mode.width//2, mode.height//2, text = mode.displayText, fill = color, font = "Phosphate 40 bold")
        # create the header
        canvas.create_text(mode.width//2, mode.height//6, text = "HELP MODE", fill = 'hotpink', font = "Phosphate 150 bold")
        # draw the police speaking
        textCX = mode.width//4*3-50
        canvas.create_image(mode.width//4-50, mode.height//2, image=ImageTk.PhotoImage(mode.police))
        canvas.create_image(textCX, mode.height//2, image=ImageTk.PhotoImage(mode.woodenSign))
        canvas.create_text(textCX, mode.height//2, text = mode.displayText, fill = 'brown', font = "Phosphate 40 bold")

        canvas.create_text(mode.width//2, mode.height//6*5, text = "Use arrow keys to move\n   between instructions", fill = 'cyan', font = "Phosphate 40 bold")
        canvas.create_text(mode.width//2, mode.height-50, text = "Press H to return", fill = 'pink', font = "Phosphate 40 bold")



