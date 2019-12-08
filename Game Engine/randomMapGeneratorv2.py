# Citation: I am using the 15-112 coursenotes animation framework
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

# creates road pieces that will be pieces together
# updates
# fully implemented bounds collision checks

from cmu_112_graphics import *
from tkinter import *
import random

class RoadPieces(object):
    # cx refers
    def __init__(self, cx, cy, roadWidth):
        # cx and cy refers to the bottom centre coordinates of the road
        self.cx = cx
        self.cy = cy
        self.roadWidth = roadWidth
        self.roadHeight = 3*roadWidth
        # appends new piece once created

    def detectOutOfBounds(self, playerCX, playerCY):
        # other classes super inherit
        pass

    def currentPiece(self, playerCX, playerCY):
        pass

class StraightPiece(RoadPieces):
    # returns the rectangular coordinates of the box
    def getStraightPiece(self):
        x0, x1 = self.cx - self.roadWidth//2, self.cx + self.roadWidth//2
        y0, y1 = self.cy, self.cy - self.roadHeight
        return (x0, y0, x1, y1)

    def detectOutOfBounds(self, playerCX, playerCY, offset = 0):
        leftBound, rightBound = self.cx - self.roadWidth//2, self.cx + self.roadWidth//2
        if leftBound + offset < playerCX < rightBound - offset:
            return False
        return True

class StartingPiece(StraightPiece):
    def getRibbonBox(self):
        x0, x1 = self.cx - self.roadWidth//2, self.cx + self.roadWidth//2
        y0, y1 = self.cy - 100, self.cy - 200
        return x0, y0, x1, y1

class EndPiece(StraightPiece):
    def getRibbonBox(self):
        x0, x1 = self.cx - self.roadWidth//2, self.cx + self.roadWidth//2
        y0, y1 = self.cy - 700, self.cy - 800
        return x0, y0, x1, y1

class RightTurnPiece(RoadPieces):
    def __init__(self, cx, cy, roadWidth):
        super().__init__(cx, cy, roadWidth)
        self.roadHeight = 2 * self.roadWidth
    
    # returns the rectangular coordinates of the box
    def getRightTurnPiece(self):
        # smaller arc
        cx, cy = self.cx + self.roadWidth, self.cy
        radius = self.roadWidth//2
        x0, x1 = cx - radius, cx + radius
        y0, y1 = cy - radius, cy + radius

        # larger arc
        radius = (self.roadWidth//2)*3
        x2, x3 = cx - radius, cx + radius
        y2, y3 = cy - radius, cy + radius

        # drawing back to straight road
        # smaller arc
        cx, cy = cx, self.cy - self.roadWidth*2
        radius = self.roadWidth//2
        x4, x5 = cx - radius, cx + radius
        y4, y5 = cy - radius, cy + radius

        # larger arc
        radius = (self.roadWidth//2)*3
        x6, x7 = cx - radius, cx + radius
        y6, y7 = cy - radius, cy + radius

        return (x0, y0, x1, y1), (x2, y2, x3, y3), (x4, y4, x5, y5), (x6, y6, x7, y7)

    def detectOutOfBounds(self, playerCX, playerCY, offset = 0):
        # the right turn comprises of 2 half circles
        # need to determine which half the circle is in

        # within the right turn
        # player position is lower half of the turn if before 
        # leftside of the split middle (aka virtual CX)
        virtualCX = self.cx + self.roadWidth
        if playerCX < virtualCX:
            virtualCY = self.cy
            # print('Part 1')
        # within the turn back
        else:
            virtualCY = self.cy - self.roadWidth*2
            # print('Part 2')
        
        dist = ((playerCX - virtualCX)**2 + (playerCY - virtualCY)**2)**0.5
        if dist < self.roadWidth//2 + offset:
            return True
        elif dist > 3*self.roadWidth//2 - offset:
            return True
        return False

class LeftTurnPiece(RoadPieces):
    def __init__(self, cx, cy, roadWidth):
        super().__init__(cx, cy, roadWidth)
        self.roadHeight = 2 * self.roadWidth

    # returns the rectangular coordinates of the box
    def getLeftTurnPiece(self):
        # smaller arc
        cx, cy = self.cx - self.roadWidth, self.cy
        radius = self.roadWidth//2
        x0, x1 = cx - radius, cx + radius
        y0, y1 = cy - radius, cy + radius

        # larger arc
        radius = (self.roadWidth//2)*3
        x2, x3 = cx - radius, cx + radius
        y2, y3 = cy - radius, cy + radius

        # drawing back to straight road
        # smaller arc
        cx, cy = cx, self.cy - self.roadWidth*2
        radius = self.roadWidth//2
        x4, x5 = cx - radius, cx + radius
        y4, y5 = cy - radius, cy + radius

        # larger arc
        radius = (self.roadWidth//2)*3
        x6, x7 = cx - radius, cx + radius
        y6, y7 = cy - radius, cy + radius

        return (x0, y0, x1, y1), (x2, y2, x3, y3), (x4, y4, x5, y5), (x6, y6, x7, y7)

    def detectOutOfBounds(self, playerCX, playerCY, offset = 0):
        # the right turn comprises of 2 half circles
        # need to determine which half the circle is in

        # within the right turn
        # player position is lower half of the turn if before 
        # leftside of the split middle (aka virtual CX)
        virtualCX = self.cx - self.roadWidth
        if playerCX > virtualCX:
            virtualCY = self.cy
            # print('Part 1')
        # within the turn back
        else:
            virtualCY = self.cy - self.roadWidth*2
            # print('Part 2')
        
        dist = ((playerCX - virtualCX)**2 + (playerCY - virtualCY)**2)**0.5
        if dist < self.roadWidth//2 + offset:
            return True
        elif dist > 3*self.roadWidth//2 - offset:
            return True
        return False

class Shrub(object):
    def __init__(self, cx, cy, image):
        self.cx = cx
        self.cy = cy
        self.image = image

    # from 112 course notes on cached images
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def drawShrub(self, canvas):
        image = self.getCachedPhotoImage(self.image)
        canvas.create_image(self.cx, self.cy, image = image)

class RandomRoadGenerator(object):
    def __init__(self, canvasHeight, canvasWidth, shrubImg, numRoadPieces = 50):
        i = 0
        startX, startY = canvasWidth//2, canvasHeight
        self.shrubs = []
        self.roadPieces = []
        # road is 80% of screen size
        self.roadWidth = canvasWidth*0.6
        self.numRoadPieces = numRoadPieces
        self.shrubImg = shrubImg
        self.shrubSize = shrubImg.size
        # 10 LP, 10 RP and 15 SP (including start and end)
        while i < self.numRoadPieces:
            pieces = ["s", "r", "l"]
            # print(i, self.numRoadPieces)
            # game always start with a start piece
            if i == 0:
                startPiece = StartingPiece(startX, startY, self.roadWidth)
                self.roadPieces.append(startPiece)
                shrub = Shrub(startX - self.roadWidth//2 - self.shrubSize[0], startY - 100, self.shrubImg)
                self.shrubs.append(shrub)
                shrub = Shrub(startX + self.roadWidth//2 + self.shrubSize[0], startY - 400, self.shrubImg)
                self.shrubs.append(shrub)
                startY -= startPiece.roadHeight
            elif i == self.numRoadPieces - 1:
                endPiece = EndPiece(startX, startY, self.roadWidth)
                self.roadPieces.append(endPiece)
                shrub = Shrub(startX - self.roadWidth//2 - self.shrubSize[0], startY - 100, self.shrubImg)
                self.shrubs.append(shrub)
                shrub = Shrub(startX + self.roadWidth//2 + self.shrubSize[0], startY - 400, self.shrubImg)
                self.shrubs.append(shrub)
                startY -= endPiece.roadHeight
            else:
                piece = random.choice(pieces)
                # check if this piece exceeds the number required
                if self.exceedingPieces(self.roadPieces, piece):
                    continue
                elif piece == 's':
                    straightPiece = StraightPiece(startX, startY, self.roadWidth)
                    self.roadPieces.append(straightPiece)
                    shrub = Shrub(startX - self.roadWidth//2 - self.shrubSize[0], startY - 400, self.shrubImg)
                    self.shrubs.append(shrub)
                    shrub = Shrub(startX + self.roadWidth//2 + self.shrubSize[0], startY - 1000, self.shrubImg)
                    self.shrubs.append(shrub)
                    startY -= straightPiece.roadHeight
                elif piece == 'r':
                    rightTurnPiece = RightTurnPiece(startX, startY, self.roadWidth)
                    self.roadPieces.append(rightTurnPiece)
                    shrub = Shrub(startX + self.roadWidth//2 + self.shrubSize[0], startY - 200, self.shrubImg)
                    self.shrubs.append(shrub)
                    shrub = Shrub(startX + self.roadWidth//2 + self.shrubSize[0], startY - 1000, self.shrubImg)
                    self.shrubs.append(shrub)
                    startY -= rightTurnPiece.roadHeight
                    startX += rightTurnPiece.roadWidth * 2
                else:
                    leftTurnPiece = LeftTurnPiece(startX, startY, self.roadWidth)
                    self.roadPieces.append(leftTurnPiece)
                    shrub = Shrub(startX - self.roadWidth//2 - self.shrubSize[0], startY - 200, self.shrubImg)
                    self.shrubs.append(shrub)
                    shrub = Shrub(startX - self.roadWidth//2 - self.shrubSize[0], startY - 1000, self.shrubImg)
                    self.shrubs.append(shrub)
                    startY -= leftTurnPiece.roadHeight
                    startX -= leftTurnPiece.roadWidth * 2
            i += 1
        self.totalDistance = startY

    # counting the number of pieces so far
    def countPieces(self, pieces):
        sp, lp, rp = 0, 0, 0
        for piece in pieces:
            if isinstance(piece, StraightPiece):
                sp += 1
            elif isinstance(piece, LeftTurnPiece):
                lp += 1
            elif isinstance(piece, RightTurnPiece):
                rp += 1
        # print(sp, lp, rp)
        return (sp, lp, rp)

    # determines whether to add this piece
    # fixes the total road distance to 40km
    def exceedingPieces(self, pieces, piece):
        (sp, lp, rp) = self.countPieces(pieces)
        # print(sp, lp, rp)
        if sp == 14 and piece == 's':
            # print('1')
            return True
        elif lp == 10 and piece == 'l':
            # print('2')
            return True
        elif rp == 10 and piece == 'r':
            # print('3')
            return True
        # print('4', piece)
        return False

    def getRandomRoad(self):
        return self.roadPieces

    def getShrubs(self):
        return self.shrubs

    @staticmethod
    def getRoadPiece(roadPieces, CarY):
        for piece in roadPieces:
            yLower = piece.cy
            yUpper = piece.cy - piece.roadHeight
            if yUpper <= CarY <= yLower:
                return piece
        return None

    def getTotalDistance(self):
        return abs(self.totalDistance)

# ########################
# # TEST FUNCTIONS
# ########################

# # drawing the road pieces
# def appStarted(app):
#     # initialising 10 default road pieces
#     i = 0
#     pieces = ["s", "r", "l"]
#     startX, startY = app.width//2, app.height
#     app.roadPieces = []
#     app.roadWidth = app.width*0.8
#     roadPieces = 50
#     while i < 50:
#         piece = random.choice(pieces)

#         # piece = pieces[i%3]
#         if piece == 's':
#             straightPiece = StraightPiece(startX, startY, app.roadWidth)
#             app.roadPieces.append(straightPiece)
#             startY -= straightPiece.roadHeight
#         elif piece == 'r':
#             rightTurnPiece = RightTurnPiece(startX, startY, app.roadWidth)
#             app.roadPieces.append(rightTurnPiece)
#             startY -= rightTurnPiece.roadHeight
#             startX += rightTurnPiece.roadWidth * 2
#         else:
#             leftTurnPiece = LeftTurnPiece(startX, startY, app.roadWidth)
#             app.roadPieces.append(leftTurnPiece)
#             startY -= leftTurnPiece.roadHeight
#             startX -= leftTurnPiece.roadWidth * 2
#         i += 1
#     app.speed = 2
#     app.timerDelay = 10
#     app.currDistance = 0
#     app.currentPiece = None
#     app.time = 0

#     app.playerX, app.playerY = app.width//2, app.height-80

# def redrawAll(app, canvas):
#     for roadPiece in app.roadPieces:
#         if isinstance(roadPiece, StraightPiece):
#             p1 = roadPiece.getStraightPiece()
#             canvas.create_rectangle(p1, fill = 'black')

#         elif isinstance(roadPiece, RightTurnPiece):
#             p1, p2, p3, p4 = roadPiece.getRightTurnPiece()
#             canvas.create_arc(p2, fill = 'black', start = 90, outline = 'black')
#             canvas.create_arc(p1, fill = 'white', start = 90, outline = 'white')
#             canvas.create_arc(p4, fill = 'black', start = 270, outline = 'black')
#             canvas.create_arc(p3, fill = 'white', start = 270, outline = 'white')

#         else:
#             p1, p2, p3, p4 = roadPiece.getLeftTurnPiece()
#             canvas.create_arc(p2, fill = 'black', start = 0, outline = 'black')
#             canvas.create_arc(p1, fill = 'white', start = 0, outline = 'white')
#             canvas.create_arc(p4, fill = 'black', start = 180, outline = 'black')
#             canvas.create_arc(p3, fill = 'white', start = 180, outline = 'white')

#     # drawing the player
#     length, width, color = 100, 60, 'blue'
#     x0, y0 = app.playerX - width//2, app.playerY - length//2
#     x1, y1 = app.playerX + width//2, app.playerY + length//2 
#     canvas.create_rectangle(x0, y0, x1, y1, fill = color)

# def keyPressed(app, event):
#     # moving the pices horizontally
#     if event.key == "Left":
#         for roadPiece in app.roadPieces:
#             roadPiece.cx += 20
#     if event.key == "Right":
#         for roadPiece in app.roadPieces:
#             roadPiece.cx -= 20
#     if event.key == "Up":
#         for roadPiece in app.roadPieces:
#             roadPiece.cy += 50
#     if event.key == "Down":
#         for roadPiece in app.roadPieces:
#             roadPiece.cy -= 50

# def timerFired(app):
#     # app.currDistance += app.speed
#     app.time += app.timerDelay
#     for roadPiece in app.roadPieces:

#         # detects the current piece within of the each specific piece range
#         if roadPiece.cy - roadPiece.roadHeight < app.playerY < roadPiece.cy:
#             app.currentPiece = roadPiece

#         # move each piece based on the speed
#         roadPiece.cy += app.speed

#     print(app.currentPiece)
#     # test function to see car current position
#     if isinstance(app.currentPiece, RightTurnPiece):
#         print(app.currentPiece.detectOutOfBounds(app.width//2, app.height))

# runApp(width = 500, height = 500)




