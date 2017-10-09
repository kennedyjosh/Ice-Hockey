import pygame
from math import *
from constants import *

# this class controls the puck (duh)
class Puck:
    #initialize
    def __init__(self,img,w,h):
        self.width, self.height = w,h
        self.img = img
        self.vx, self.vy = 0,0
        self.spd = 2
        self.x,self.y = -690,-690
        self.fricTrack = 0
        self.vxStored, self.vyStored = 0,0
   
    # return a rectangle of the IMAGE (not technically the puck itself - the x/y will be wrong)
    # use this only for width & height
    # ^I admit that it was stupid to have this misleading getRect function that returns an incorrect
    # x/y value, but the mistake went too deep before I thought to fix it
    def getRect(self):
        return self.img.get_rect()
                
    # used only in very early stages, this let the puck be moved by user input
    def getInput(self):
        p = pygame.key.get_pressed()
        if p[pygame.K_UP] or p[pygame.K_w]:
            self.vy -= self.spd
        elif p[pygame.K_DOWN] or p[pygame.K_s]:
            self.vy += self.spd
        if p[pygame.K_LEFT] or p[pygame.K_a]:
            self.vx -= self.spd
        elif p[pygame.K_RIGHT] or p[pygame.K_d]:
            self.vx += self.spd
        
        if self.vx != 0 and self.vy != 0:
            self.vx *= .5
            self.vy *= .5
    
    # get the location of the puck on the rink
    def getLoc(self, rink):
        return rink.getLoc(self)
    
    # apply puck's velocities to its position
    def move(self, rink):
        #reset puck to center ice if not on ice surface
        if self.x < 0 or self.y < 0:
            middleX = rink.borderList[rink.getIndex("rm")].getRect().center[0]
            middleY = rink.borderList[rink.getIndex("rm")].getRect().center[1]
            self.x,self.y = middleX-self.getRect().width/2,middleY-self.getRect().height/2
        #perform movement, if you can
        if self.vx < 0:
            if not self.doesBorderExistLeft(rink):
                self.x += getAdjustedValue(self.vx)
            else:
                self.vx *= -1
                self.x += getAdjustedValue(self.vx)
        elif self.vx > 0:
            if not self.doesBorderExistRight(rink):
                self.x += getAdjustedValue(self.vx)
            else:
                self.vx *= -1
                self.x += getAdjustedValue(self.vx)

        if self.vy < 0:
            if not self.doesBorderExistUp(rink):
                self.y += getAdjustedValue(self.vy)
            else:
                self.vy *= -1
                self.y +=  getAdjustedValue(self.vy)
        elif self.vy > 0:
            if not self.doesBorderExistDown(rink):
                self.y += getAdjustedValue(self.vy)
            else:
                self.vy *= -1
                self.y += getAdjustedValue(self.vy)
        
    # function to ensure puck does not leave the top of the rink
    def doesBorderExistUp(self, rink):
        ## Check for border only when puck is moving up
        ## return True if border exists
        ## return False if no border and movement is allowed
        m = self
        ## above variables are to simplify code
        
        # top left circle
        bTL = rink.borderList[rink.getIndex("ctl")].getRect()
        cTL = bTL.center
        distFromCenterTL = ((m.x-cTL[0])**2 + (m.y-cTL[1])**2)**.5
        if m.x < bTL.x+bTL.width/2:                # puck is on correct side of ice
            if m.x < cTL[0] and m.y <= cTL[1]:       # puck is in correct quadrant
                if distFromCenterTL > (bTL.width/2):      # check if puck is on edge
                    return True
        
        # top right circle
        bTR = rink.borderList[rink.getIndex("ctr")].getRect()
        cTR = bTR.center
        distFromCenterTR = (((m.x+m.width)-cTR[0])**2 + ((m.y)-cTR[1])**2)**.5
        if m.x > bTR.x:                                 # puck is on correct side of ice
            if m.x+m.width >= cTR[0] and m.y+m.height <= cTR[1]:   # puck is in correct quadrant
                if distFromCenterTR > (bTR.width/2):       # check if puck is on edge
                    return True
        
        # rect
        bU = rink.borderList[rink.getIndex('rm')].getRect()
        if m.y <= bU.y:         #check if y is on edge
            return True
                
        #if all else fails you can move, return False
        return False
                
    # function to ensure puck does not leave the bottom of the rink
    def doesBorderExistDown(self, rink):
        ## Check for border only when puck is moving down
        ## return True if border exists 
        ## return False if no border and movement is allowed
        m = self
        ## above variables are to simplify code
        
        # bottom left circle
        bBL = rink.borderList[rink.getIndex("cbl")].getRect()
        cBL = bBL.center
        distFromCenter = ((m.x-cBL[0])**2 + ((m.y+m.height)-cBL[1])**2)**.5
        if m.x < bBL.x+bBL.width/2:                # puck is on correct side of ice
            if m.x <= cBL[0] and m.y >= cBL[1]:       # puck is in correct quadrant
                if distFromCenter >= (bBL.width/2):      # check if puck is on edge
                    return True
            
        # bottom right circle
        bBR = rink.borderList[rink.getIndex('cbr')].getRect()
        cBR = bBR.center
        distFromCenter = (((m.x+m.width)-cBR[0])**2 + ((m.y+m.height)-cBR[1])**2)**.5
        if m.x > bBR.x:                                # puck is on correct side of ice
            if m.x >= cBR[0] and m.y >= cBR[1]:   # puck is in correct quadrant
                if distFromCenter >= (bBR.height/2):       # check if puck is on edge
                    return True
            
        # middle rect
        bD = rink.borderList[rink.getIndex('rm')].getRect()
        if bD.x <= m.x+m.width <= bD.x+bD.width:    #check if within rect
            if m.y+m.height >= bD.y+bD.height:         #check if y is on edge
                return True
                
        #if all else fails, you can move, return False
        return False

    # function to ensure puck does not leave the left of the rink
    def doesBorderExistLeft(self, rink):
        ## Check for border only when puck is moving left
        ## return True if border exists
        ## return False if no border and movement is allowed
        m = self
        ## above variables are to simplify code
        
        # top left circle
        bTL = rink.borderList[rink.getIndex('ctl')].getRect()
        cTL = bTL.center
        distFromCenter = ((m.x-cTL[0])**2 + (m.y-cTL[1])**2)**.5
        if m.x < bTL.x+bTL.width/2:                # puck is on correct side of ice
            if m.x <= cTL[0] and m.y <= cTL[1]:       # puck is in correct quadrant
                if distFromCenter >= (bTL.width/2):      # check if puck is on edge
                    return True
            
        # bottom left circle
        bBL = rink.borderList[rink.getIndex('cbl')].getRect()
        cBL = bBL.center
        distFromCenter = (((m.x)-cBL[0])**2 + ((m.y+m.height)-cBL[1])**2)**.5
        if m.x < bBL.x+bBL.width/2:                # puck is on correct side of ice
            if m.x <= cBL[0] and m.y >= cBL[1]:   # puck is in correct quadrant
                if distFromCenter >= (bBL.width/2):       #check if puck is on edge
                    return True
            
        # middle rect
        bL = rink.borderList[rink.getIndex('rm')].getRect()
        if bL.y <= m.y <= bL.y+bL.height:    #check if within rect
            if m.x <= bL.x:         #check if x is on edge
                return True
                
        #if all else fails, you can move, return False
        return False
    
    # function to ensure puck does not leave the right of the rink
    def doesBorderExistRight(self, rink):
        ## Check for border only when puck is moving right
        ## return True if border exists
        ## return False if no border and movement is allowed
        m = self
        ## above variables are to simplify code
        
        # top right circle
        bTR = rink.borderList[rink.getIndex('ctr')].getRect()
        cTR = bTR.center
        distFromCenter = (((m.x+m.width)-cTR[0])**2 + (m.y-cTR[1])**2)**.5
        if m.x > bTR.x:
            if m.x >= cTR[0] and m.y <= cTR[1]:       # puck is in correct quadrant
                if distFromCenter >= (bTR.width/2):      # check if puck is on edge
                    return True
            
        # bottom right circle
        bBR = rink.borderList[rink.getIndex('cbr')].getRect()
        cBR = bBR.center
        distFromCenter = (((m.x+m.width)-cBR[0])**2 + ((m.y+m.height)-cBR[1])**2)**.5
        if m.x > bBR.x:
            if m.x >= cBR[0] and m.y >= cBR[1]:   # puck is in correct quadrant
                if distFromCenter >= (bBR.width/2):       #check if puck is on edge
                    return True
            
        # right rect
        bR = rink.borderList[rink.getIndex('rm')].getRect()
        if bR.y <= m.y <= bR.y+bR.height:    #check if within rect
            if m.x+m.width >= bR.x+bR.width:         #check if x is on edge
                return True
                
        #if all else fails, you can move, return False
        return False
        
    # apply friction to puck if puck is moving
    def applyFriction(self):
        # I may have overcomplicated this a bit, but it works, so... it is what it is
        if self.vy > 0 and self.vx > 0:
            self.vx += FRICTION/2
            self.vy += FRICTION/2
            self.fricTrack += FRICTION /2
        elif self.vy < 0 and self.vx < 0:
            self.vx -= FRICTION/2
            self.vy -= FRICTION/2
            self.fricTrack += FRICTION
        elif self.vy > 0 and self.vx < 0:
            self.vx -= FRICTION/2
            self.vy += FRICTION/2
            self.fricTrack += FRICTION
        elif self.vy < 0 and self.vx > 0:
            self.vx += FRICTION/2
            self.vy -= FRICTION/2
            self.fricTrack += FRICTION
        elif self.vx > 0 and self.vy == 0:
            self.vx += FRICTION
            self.fricTrack += FRICTION
        elif self.vx < 0 and self.vy == 0:
            self.vx -= FRICTION
            self.fricTrack += FRICTION
        elif self.vy > 0 and self.vx == 0:
            self.vy += FRICTION
            self.fricTrack += FRICTION
        elif self.vy < 0 and self.vx == 0:
            self.vy -= FRICTION
            self.fricTrack += FRICTION    
    
    # update the puck's information
    def update(self, screen, rink):
        #set speed so that it is the same no matter the framerate
        self.spd = getAdjustedValue(7)
        
        #allow the puck to move based on player input
        # obviously this feature has been disabled
#         self.getInput()

        #apply friction
        self.applyFriction()

#         print "Friction tracker =",self.fricTrack,"| vx/vy stored (rounded) =",round(self.vxStored,2),round(self.vyStored,2)
#         if self.fricTrack == round(self.vxStored,2) or self.fricTrack == round(self.vyStored,2):
        if round(self.vx,2) == 0 and round(self.vy,2) == 0:
            self.vx, self.vy = 0,0
            self.fricTrack = 0
            self.vxStored, self.vyStored = 0,0

        # add puck velocities to its position
        self.move(rink)
        
        #draw puck on screen
        screen.blit(self.img, (self.x,self.y))
        
        