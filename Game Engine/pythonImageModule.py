"""
# IDEA
1. USER CAN EITHER UPLOAD THEIR IMAGE
2. CHOOSE A CUSTOM CAR, BUT THE COLOR AND DESIGN OF THE CAR IS CUSTOMIZABLE
"""
from PIL import Image, ImageDraw
from cmu_112_graphics import *
from tkinter import *
import os
import random
import copy

class Shapes(object):
    def __init__(self, cx, cy, width, length, color):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.length = length
        self.color = color

    def getCorners(self):
        # get a rectangular estimate of the corners
        x0, x1 = self.cx - self.width//2, self.cx + self.width//2
        y0, y1 = self.cy - self.length//2, self.cy + self.length//2
        return x0, y0, x1, y1

    @staticmethod
    # pass in a list of x and y coords
    def getMaxCorners(xVals, yVals):
        return min(xVals), min(yVals), max(xVals), max(yVals)
        
class Rectangle(Shapes):
    def draw(self, canvas):
        cx, cy, color = self.cx, self.cy, self.color
        length, width = self.length, self.width

        x0, y0 = cx - width//2, cy - length//2
        x1, y1 = cx + width//2, cy + length//2
        canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = color)

class Ellipse(Shapes):
    def draw(self, canvas):
        cx, cy, color = self.cx, self.cy, self.color
        length, width = self.length, self.width

        x0, y0 = cx - width//2, cy - length//2
        x1, y1 = cx + width//2, cy + length//2
        canvas.create_oval(x0, y0, x1, y1, fill = color, outline = color)

class Triangle(Shapes):
    def draw(self, canvas):
        x0, y0 = self.cx - self.width//2, self.cy + self.length//2
        x1, y1 = self.cx + self.width//2, self.cy + self.length//2
        x2, y2 = self.cx, self.cy - self.length//2
        color = self.color
        canvas.create_polygon(x0, y0, x1, y1, x2, y2, fill = color, outline = color)

class CustomCarMode(Mode):
    def appStarted(mode):
        mode.shapes = []
        mode.selectedShape = None
        # mode.initUserCar()
        mode.shapeCreated = False
        # print(mode.width, mode.height)
        mode.creatingShape = False
        mode.keyPad = []
        mode.doneFlag = False
        mode.numCars = 5
        mode.takeScreenShots = False
        mode.time = 0
        mode.displayedVersion = None
        mode.initTkinterColors()

    # taken from http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    def initTkinterColors(mode):
        mode.colors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99', 'black', 'green', 'red', 'yellow',
    'blue', 'hotpink']

    # ask the user if he would like to create a custom car
    def initUserCar(mode):
        # isCustom = input("Do you have a image to upload?")
        isCustom = True
        # if car is custom design
        if isCustom:
            img = mode.createShape()
        else:
            pass
        return img

    def getCroppedBox(mode):
        # instantiate empty lists to store the coordinates
        xVals, yVals = [], []
        for shape in mode.shapes:
            x0, y0, x1, y1 = shape.getCorners()
            xVals.extend([x0, x1])
            yVals.extend([y0, y1])
        return Shapes.getMaxCorners(xVals, yVals)

    def timerFired(mode):
        if mode.takeScreenShots:
            # append the player Car so a ss can be taken
            mode.otherCars.append(mode.shapes)
            clocktick = (mode.time//mode.timerDelay)
            index = clocktick//2
            # print(index, clocktick)
            # once the index exceeds the number of cars plus player, break
            if index >= mode.numCars + 1:
                mode.takeScreenShots = False
                # ADD CHANGE MODE HERE
                mode.app.setActiveMode(mode.app.gameMode)
                return
            # at every rising edge of the clock tick, change the display image
            elif clocktick%2 == 0:
                mode.displayedVersion = mode.otherCars[index]
            # at every falling edge of clock tick, take the screenshot
            elif clocktick%2 == 1:
                mode.image = mode.filterImg(mode.app.getSnapshot())
                # take the screenshot of the player car before ending the process
                if index == mode.numCars:
                    filename = "customPlayerCar.png"
                else:
                    filename = f"customCar_{index}.png"
                parentDir = os.path.abspath("..")
                img_dir = os.path.join(parentDir, f"Pictures/{filename}")
                mode.image.save(img_dir, 'png')
            mode.time += mode.timerDelay

    def randomizeCars(mode, shapes, numCars = 5):
        newCars = []
        for i in range(numCars):
            randomColors = copy.deepcopy(mode.colors)
            triangleColor = random.choice(randomColors)
            randomColors.remove(triangleColor)
            ellipseColor = random.choice(randomColors)
            randomColors.remove(ellipseColor)
            rectangleColor = random.choice(randomColors)
            newCar = []
            for shape in shapes:
                newShape = copy.deepcopy(shape)
                if isinstance(newShape, Rectangle):
                    newShape.color = rectangleColor
                elif isinstance(newShape, Ellipse):
                    newShape.color = ellipseColor
                elif isinstance(newShape, Triangle):
                    newShape.color = triangleColor
                newCar.append(newShape)
            newCars.append(newCar)
        return newCars

    def keyPressed(mode, event):
        # forbidden keys
        if mode.selectedShape == None and event.key in ["Up", "Down", "Left", "Right"]:
            pass
        elif event.key == 'control-1' and mode.shapes != []:
            mode.otherCars = mode.randomizeCars(mode.shapes)
            mode.takeScreenShots = True

        elif event.key == 'control-1' and mode.shapes == []:
            print("CREATE CUSTOM CAR FIRST!")

        elif mode.selectedShape != None:
            if event.key == "Up":
                mode.selectedShape.length += 10
            elif event.key == "Down":
                if mode.selectedShape.length > 10:
                    mode.selectedShape.length -= 10
            elif event.key == "Right":
                mode.selectedShape.width += 10
            elif event.key == "Left":
                if mode.selectedShape.width > 10:
                    mode.selectedShape.width -= 10
            elif event.key == 'Delete':
                if len(mode.shapes) > 0:
                    mode.shapes.remove(mode.selectedShape)
        
        elif event.key == "Enter":
            try:
                color, text = "".join(mode.keyPad).lower().split(" ")
            # if random words
            except:
                mode.keyPad = []
                return
            text = text.strip()
            color = color.strip()
            if color not in mode.colors:
                mode.keyPad = []
                return
            shape = None
            cx, cy = mode.width//2, mode.height//2
            if text in ["rect", "rectangle", "square"]:
                shape = Rectangle(cx, cy, 50, 100, color)
            elif text in ["cir", "circle", "ellipse"]:
                shape = Ellipse(cx, cy, 50, 50, color)
            elif text in ['tri', 'triangle']:
                shape = Triangle(cx, cy, 50, 50, color)
            if isinstance(shape, Shapes):
                mode.shapes.append(shape)
            mode.keyPad = []

        elif event.key == "Space":
            mode.keyPad.append(" ")
        elif event.key == "Delete":
            if len(mode.keyPad) > 0:
                mode.keyPad.pop()
        else:
            mode.keyPad.append(event.key)

    # code reference from 
    # https://stackoverflow.com/questions/52145972/remove-image-background-and-create-a-transparent-image-using-pythons-pil
    def filterImg(mode, img):
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        # get the dimensions of the snapshot and scale it back to the dimensions of this canvas
        width, height = img.size
        ratio = mode.width/width
        scaledImg = mode.scaleImage(img, ratio)
        # finding the dimensions of the image to crop
        left, top, right, bottom = mode.getCroppedBox()
        # scaledImg.show()
        scaledImg = scaledImg.crop((left, top, right, bottom))
        return scaledImg

    def createShape(mode):
        while True:
            shape = input("What Shape? ")
            print('yo')
            color = input("What Color? ")
            if shape.lower() == "rectangle":
                rect = Rectangle(mode.width//2, mode.height//2, 20, 50, color)
                return rect
            elif shape.lower() in ['circle', 'ellipse']:
                ellipse = Ellipse(mode.width//2, mode.height//2, 20, 50, color)
                return ellipse

    def mousePressed(mode, event):
        mouseX, mouseY = event.x, event.y
        # print(mouseX, mouseY)
        # selecting shape based on layer order (last one first)
        for shape in mode.shapes[::-1]:
            cx, cy = shape.cx, shape.cy
            # print(cx, cy)
            length, width = shape.length, shape.width
            x0, y0 = cx - width//2, cy - length//2
            x1, y1 = cx + width//2, cy + length//2
            if x0 < mouseX < x1 and y0 < mouseY < y1:
                mode.selectedShape = shape
                break

    def mouseDragged(mode, event):
        shape = mode.selectedShape
        if shape != None:
            shape.cx = event.x
            shape.cy = event.y

    def mouseReleased(mode, event):
        mode.selectedShape = None

    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'black')
        x0, x1 = mode.width//4, mode.width*3//4
        y0, y1 = mode.height//4, mode.height*3//4
        canvas.create_rectangle(x0, y0, x1, y1, fill = 'white')
        # canvas.create_rectangle(0, 0, mode.width, mode.height, fill = 'black')
        if mode.takeScreenShots == False:
            # include the instructions here
            line1 = "VEHICLE MAKERSPACE"
            line2 = "Type the color follow by the shape and click enter!"
            line3 = "Click on shape and use arrow keys to adjust size"
            line4 = "Click on shape and press delete to remove shape"
            line5 = "Once you are done, press ctrl-1 to save the screenshot!"
            canvas.create_text(mode.width//2, 100, text = line1, font = "Phosphate 80 bold", fill = 'springgreen2')
            canvas.create_text(mode.width//2, mode.height - 160, text = line2, font = "Phosphate 25 bold", fill = 'hotpink')
            canvas.create_text(mode.width//2, mode.height - 120, text = line3, font = "Phosphate 25 bold", fill = 'cyan')
            canvas.create_text(mode.width//2, mode.height - 80, text = line4, font = "Phosphate 25 bold", fill = 'goldenrod2')
            canvas.create_text(mode.width//2, mode.height - 40, text = line5, font = "Phosphate 25 bold", fill = 'slateblue1')
            for shape in mode.shapes:
                try:
                    shape.draw(canvas)
                except:
                    continue

            cx, cy = mode.width//2, mode.height//2
            text = "".join(mode.keyPad)
            canvas.create_text(cx, cy, text = text, font = "Phosphate 50 bold")

        # if it is in take screenshot mode
        else:
            # tell the user to not exit
            text = "GENERATING ENEMY CARS..."
            canvas.create_text(mode.width//2, 50, text = text, font = "Phosphate 50 bold", fill = 'springgreen2')
            if mode.displayedVersion != None:
                for shape in mode.displayedVersion:
                    shape.draw(canvas)

# class MyModalApp(ModalApp):
#     def appStarted(app):
#         app.customScreen = CustomCarMode()
#         app.setActiveMode(app.customScreen)

# app = MyModalApp(width=600, height=600)



