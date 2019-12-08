# random car generator
from tkinter import *
from cmu_112_graphics import *
from randomMapGeneratorv2 import RandomRoadGenerator, StraightPiece, LeftTurnPiece, RightTurnPiece
import random
import math

class Car(object):
    def __init__(self, cx, cy, length, width, color, speed = 10, image = None, rotate = 0, cache = True):
        self.cx = cx
        self.cy = cy
        self.color = color
        self.speed = speed
        self.rotate = rotate
        # player car should not be cached, since it is constantly rotating
        if cache == False:
            self.image = image
        else:
            self.image = image.rotate((self.rotate/math.pi)*180, expand = True)
        if self.image != None:
            self.width, self.length = image.size
            # print(image.size)
        else:
            self.length = length
            self.width = width

    def getCarRect(self):
        if self.rotate != 0:
            # switch the x and y coordinates, as the car is now horizontal
            x0, x1 = self.cx - self.length//2, self.cx + self.length//2
            y0, y1 = self.cy - self.width//2, self.cy + self.width//2
        else:
            x0, x1 = self.cx - self.width//2, self.cx + self.width//2
            y0, y1 = self.cy - self.length//2, self.cy + self.length//2
        return x0, y0, x1, y1

    @staticmethod
    def getYIntercept(y, m, x):
        return y-m*x

    @staticmethod
    def checkLinesIntersect(Car1, Car2):
        # print('yo')
        p1, p2, p3, p4 = Car.getCornerCoords(Car1)
        # print(p1, p2, p3, p4)
        p5, p6, p7, p8 = Car.getCornerCoords(Car2)
        # print(p5, p6, p7, p8)
        # if the car is vertically oriented (meaning that the gradient is infinity)
        if (p5[0] == p6[0] and p4[0] == p3[0]) or Car1.rotate == Car2.rotate:
            # print('both vertical/parallel')
            if p5[0] <= p4[0] <= p8[0] and (p6[1] <= p4[1] <= p5[1]):
                # print('1')
                return True
            elif p1[0] <= p5[0] <= p4[0] and p3[1] <= p5[1] <= p4[1]:
                # print('2')
                return True
            return False
        elif p5[0] == p6[0]:
            x = p5[0]
            m1 = (p4[1] - p3[1]) / (p4[0] - p3[0])
            c1 = Car.getYIntercept(p4[1], m1, p4[0])
            y = m1 * x + c1
            if p6[1] <= y <= p5[1] and p3[1] <= y <= p4[1]:
                # print('3')
                return True
            return False
        elif p4[0] == p3[0]:
            x = p4[0]
            m2 = (p5[1] - p6[1]) / (p5[0] - p6[0])
            c2 = Car.getYIntercept(p5[1], m2, p5[0])
            y = m2 * x + c2
            if p3[1] <= y <= p4[1] and p6[1] <= y <= p5[1]:
                # print('4')
                return True
            return False
        else:
            # FIX THIS
            m1 = (p4[1] - p3[1]) / (p4[0] - p3[0])
            m2 = (p5[1] - p6[1]) / (p5[0] - p6[0])
            # print(m2)
            # y intercept is the y axis
            c1 = Car.getYIntercept(p3[1], m1, p3[0])
            c2 = Car.getYIntercept(p6[1], m2, p6[0])
            x = (c2-c1)/(m1-m2)
            y = m1*x + c1
            if p4[0] <= x <= p3[0] and p5[0] <= x <= p6[0]:
                # print("might work")
                if p3[1] <= y <= p4[1] and p6[1] <= y <= p5[1]:
                    # print('5')
                    return True
            return False

    @staticmethod
    # using trigonmetry to determine the coordinates of the 4 corners
    def getCornerCoords(car):
        cx, cy = car.cx, car.cy
        width, length = car.width, car.length
        # angle of rotation (need to flip as the angle is opposite)
        angle = -car.rotate
        # the components of tilted length and width
        xcomp1, xcomp2 = math.sin(angle)*(length/2), math.cos(angle)*(width/2)
        ycomp1, ycomp2 = math.cos(angle)*(length/2), math.sin(angle)*(width/2)
        p1 = (cx - xcomp1 - xcomp2, cy + ycomp1 - ycomp2)
        p2 = (cx + xcomp1 - xcomp2, cy - ycomp1 -ycomp2)
        p3 = (cx + xcomp1 + xcomp2, cy - ycomp1 + ycomp2)
        p4 = (cx - xcomp1 + xcomp2, cy + ycomp1 + ycomp2)
        return (p1, p2, p3, p4)

    # a method will loop through all the cars to check each collision
    # car 2 will by default refer to player car
    @staticmethod
    def checkCollision(Car1, Car2):
        # coordinates for car 1
        # if Car1.rotate != 0:
        #     # switch the x and y coordinates, as the car is now horizontal
        #     x0, x1 = Car1.cx - Car1.length//3, Car1.cx + Car1.length//3
        #     y0, y1 = Car1.cy - Car1.width//3, Car1.cy + Car1.width//3
        # else:
        #     x0, y0 = Car1.cx - Car1.width//2, Car1.cy - Car1.length//2
        #     x1, y1 = Car1.cx + Car1.width//2, Car1.cy + Car1.length//2 
        # # coordinates for car 2
        # if Car2.rotate != 0:
        #     x2, y2 = Car2.cx - Car2.length//3, Car2.cy - Car2.length//3
        #     x3, y3 = Car2.cx + Car2.width//3, Car2.cy + Car2.width//3
        # else:

        # this checks for basic rectangular collisions
        x0, y0 = Car1.cx - Car1.width//4, Car1.cy - Car1.length//4
        x1, y1 = Car1.cx + Car1.width//4, Car1.cy + Car1.length//4 
        x2, y2 = Car2.cx - Car2.width//4, Car2.cy - Car2.length//4
        x3, y3 = Car2.cx + Car2.width//4, Car2.cy + Car2.length//4

        # algorithm to check collision
        # 2 types of collision
        # 1. Veritcal (Front Back)
        # 2. Horizontal (Left Right)
        if x1 > x2 and x3 > x0 and (y2 < y0 < y3 or y2 < y1 < y3):
            # print('yo0')
            return True
        # else:
        #     return  False

        # this checks for sides collsion
        if Car.checkLinesIntersect(Car1, Car2):
            # print('yo1')
            return True
        elif Car.checkLinesIntersect(Car2, Car1):
            # print('yo2')
            return True
        return False

    # if the car collides with a road bound, 
    # change the dx of the car such that it will prevent the collision
    # if it collides another car, then push the front car forward
    # as the car is moving, check if it is out of bounds
    def steerCar(self, roads):
        # first increase the position of the car
        # self.cy -= self.speed
        # first find the roadPiece associated with it
        roadPiece = RandomRoadGenerator.getRoadPiece(roads, self.cy)
        # if roadPiece == None:
        #     print("Car Position:", self.cy)
        # check out of bounds
        if roadPiece.detectOutOfBounds(self.cx, self.cy):
            # try shifting it right first
            pass
            # self.cx += 5

    # from 112 course notes on cached images
    def getCachedPhotoImage(self, image):
        # stores a cached version of the PhotoImage in the PIL/Pillow image
        if ('cachedPhotoImage' not in image.__dict__):
            image.cachedPhotoImage = ImageTk.PhotoImage(image)
        return image.cachedPhotoImage

    def drawCar(self, canvas, cache = True):
        if self.image != None:
            # cached images already have fixed angle of rotation
            if cache:
                image = self.getCachedPhotoImage(self.image) 
                canvas.create_image(self.cx, self.cy, image = image)
            # player car is not cached
            # hence it respons to different angel of rotation
            else:
                canvas.create_image(self.cx, self.cy, image = ImageTk.PhotoImage(self.image.rotate((self.rotate/math.pi)*180, expand = True)))
        else:
            coords = self.getCarRect()
            canvas.create_rectangle(coords, fill = self.color)

# takes in roads to determine the current piece it is in
class RandomCarsGenerator(object):
    def __init__(self, numCars, roadDistance, roads, screenHeight, carLength, carWidth, images = None):
        self.numCars = numCars
        self.roadDistance = -roadDistance
        self.roads = roads
        # self.cars = self.generateCars()
        self.screenHeight = screenHeight
        self.carLength = carLength
        self.carWidth = carWidth
        # offset refers to the min distance between car centre and the edge
        self.CarOffset = max(self.carWidth//2, self.carLength//2)
        self.images = images

    def generateCars(self):
        # offset at least n pixels apart (in this case, they must be at least 1.5 car length apart)
        yOffset = 2.0 * self.carLength
        xOffset = 1.5 * self.carWidth
        cars = []
        i = 0
        while i < self.numCars:
            # only generate cars that are after the starting and before ending strip
            # cast the road distance to an integer
            carY = random.randint(int(self.roadDistance), 0)
            # first check if it collides with any other car
            # if it does, generate another random y value
            if self.checkYCollision(cars, carY, yOffset):
                continue
            # based on the y position of the car, find the roadpiece associated with it
            roadPiece = RandomRoadGenerator.getRoadPiece(self.roads, carY)
            if roadPiece == None:
                print(carY)
                print('error')
            else:
            # based on the piece, find the left and right bounds of the entire piece
            # generate an x position that is within this range
            # from this x and y position, do a road bounds collision check
                # print(roadPiece)
                rotate = None
                if isinstance(roadPiece, RightTurnPiece):
                    while True:
                        # loop until a point with no collision is found
                        virtualCX = roadPiece.cx + roadPiece.roadWidth
                        leftX, rightX = virtualCX - roadPiece.roadWidth*1.5, virtualCX + roadPiece.roadWidth*1.5
                        carX = random.uniform(leftX, rightX)
                        if not roadPiece.detectOutOfBounds(carX, carY, self.CarOffset):
                            rotate = "r45"
                            break
                        # print('1', leftX, rightX, virtualCX, carY)
                        # print(roadPiece.cx, roadPiece.cy, carX)

                elif isinstance(roadPiece, LeftTurnPiece):
                    while True:
                        # loop until a point with no collision is found
                        virtualCX = roadPiece.cx - roadPiece.roadWidth
                        leftX, rightX = virtualCX - roadPiece.roadWidth*1.5, virtualCX + roadPiece.roadWidth*1.5
                        carX = random.uniform(leftX, rightX)
                        if not roadPiece.detectOutOfBounds(carX, carY, self.CarOffset):
                            rotate = "l45"
                            break
                        # print('2', leftX, rightX, virtualCX, carY, carX)
                        # print(roadPiece.cx, roadPiece.cy)

                # straight road
                elif isinstance(roadPiece, StraightPiece):
                    while True:
                    # loop until a point with no collision is found
                        leftX, rightX = roadPiece.cx - roadPiece.roadWidth//2, roadPiece.cx + roadPiece.roadWidth//2
                        carX = random.uniform(leftX, rightX)
                        if not roadPiece.detectOutOfBounds(carX, carY, self.CarOffset):
                                break

                # if it passes the bounds collision check, then create this car and append to the list
                if rotate == "r45":
                    rotate = -45
                elif rotate == "l45":
                    rotate = 45
                else:
                    rotate = 0
                image = random.choice(self.images)
                car = Car(carX, carY, self.carLength, self.carWidth, "red", image = image, rotate = rotate)
                cars.append(car)
                i += 1

        # try to sort the cars based on their y positions
        return cars

    def checkYCollision(self, cars, carY, offset = 0):
        for car in cars:
            if abs(carY - car.cy) <= offset:
                return True
        return False

# TEST FUNCTIONS
# roadsGenerator = RandomRoadGenerator(500, 500, 5)
# roads = roadsGenerator.getRandomRoad()
# distance = roadsGenerator.getTotalDistance()
# print(roads)
# print("total distance:",  distance)

# cars = RandomCarsGenerator(10, distance, roads, 500).generateCars()
# print(cars)



