# This file holds everything that needs to be accessed in every file
# in the /game folder
import pygame

#screen display size
W,H = 1440, 900

# This class exists as a way to keep a contant scaling varible, Universal.c
# and also other rink measurements that I need to have ready 
class Universal:
    #Multiplier is 6 for normal use
    def __init__(self, const, topLeft):
        ## self.c = constant to apply to real-life dimensions for sclaing purposes
        self.c = const
        ## below info are real-life measurements of an NHL rink (in feet) * the amt to enlarge everything by
        self.cornerRad = (28 * self.c)                         #radius of corners
        self.cornerDia = (self.cornerRad * 2)                  #diameter of corners
        self.len, self.width = (200* self.c),(85 * self.c)               #length and width of the entire ice
        self.blueToGoal = (64 * self.c)                        #dist from blue line to goal line
        self.neutralZone = (50 * self.c)                       #length of neutral zone
        self.goalToBoards = (11 * self.c)                      #goal line to boards behind net
        self.endzoneCircRad = (15 * self.c)                    #endzone faceoff circle radius
        self.creaseRad = (4 * self.c)                          #radius of the crease, which is a semicircle
        self.betweenDots = (44 * self.c)                       #space between faceoff dots in endzone
        self.boardToBotCirc = (28 * self.c)                    #space from end boards to the bottom of the faceoff circle
        self.boardToDot = (self.len - self.betweenDots)        #dist from boards to side faceoff dots
        ## position of the top-left corner of the rink on the screen
        self.rx, self.ry = topLeft[0], topLeft[1]        


#color constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (200,0,0)
BLUE = (0,0,200)
GREEN  = (0,200,0)
LBLUE = (175,200,255)
ORANGE = (240,176,2)
YELLOW = (225,225,0)
PUREGREEN = (0,255,0)
PURERED = (255,0,0)
PUREBLUE = (0,0,255)

# friction of ice
FRICTION = -.5


#stuff to track framerate
target_tick = 0.0166667
tickval = 0


def getAdjustedValue(n):
    return n * (tickval / target_tick)

def getTickVal():
    return tickval

def updateTickVal(tv):
    global tickval
    tickval = tv
