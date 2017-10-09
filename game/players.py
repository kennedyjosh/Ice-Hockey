import pygame
from constants import *

# a class to hold the players of a team together, and to manage
# information for an individual team
class Team:
    # initialize
    def __init__(self, name, city, abbr, logo, col1, col2, playerList, universal):
        # Proper player list orders by position: C,LW,RW,LD,RD,G
        # ^ Although it isn't as important as it was in previous verisons
        self.name, self.city, self.abbr = name, city, abbr.upper()
        self.logo, self.primaryColor, self.secondaryColor = logo, col1, col2
        self.fullName = name + " " + city
        self.playerList, self.uni = playerList, universal
        self.currentPlayer = None
    
    # string version of team, in case called somewhere else
    def __str__(self):
        return self.city+' '+self.name+' ('+self.abbr+')'
        
    # 2nd initialization, in order to establish who is home and away
    # and also which team is controlled by the user
    def initialize(self, userTeam, compTeam, awayTeam, homeTeam):
        self.userTeam, self.compTeam = userTeam, compTeam
        self.awayTeam, self.homeTeam = awayTeam, homeTeam
        for p in self.playerList:
            p.img = pygame.transform.scale(p.img, (int(8*self.uni.c), int(16*self.uni.c)))
            self.startPos(None,None)
        
           
    # this function reverts the players and puck to their starting positions 
    def startPos(self,puck,screen): 
        # give user control to center if not already controlled
        if self.userTeam:
            for p in self.playerList:
                if p.pos == "C":
                    self.currentPlayer = p
        # try-catch because when first initialized, the puck doesn't exist yet
        try:           
            puck.x, puck.y = -690,-690
            puck.vx, puck.vy = 0,0
            self.fricTrack = 0
            self.vxStored, self.vyStored = 0,0
            faceoff(screen)
        except:
            pass
        
        # place players at center ice faceoff dot
        u = self.uni
        for p in self.playerList:
            p.x, p.y = 0,0
            p.vx, p.vy = 0,0
            if self.homeTeam:
                if p.pos == "C":
                    p.x = (u.rx + 114 * u.c) + p.getRect("full").x
                    p.y = (u.ry + 42.5*u.c) - p.getRect("stick").height*15
                    p.facing = "l"
                    p.homeTeam = True
            else:
                if p.pos == "C":
                    p.x = (u.rx+ 114 * u.c) - p.getRect("full").x - p.getRect("full").width
                    p.y = (u.ry + 42.5*u.c) - p.getRect("stick").height*15
                    p.facing = "r"
                    p.awayTeam = True
                    
    # this function updates every player within the team
    def update(self,screen,puck,rink):
        for p in self.playerList:
            if p is not self.currentPlayer:
                auto = True
            else:
                auto = False
            p.update(screen,puck,auto,rink)

    
# this class holds information that is individualized to the player himself/herself
class Player:
    # initialize
    ### IMPORTANT: MAKE POS = C FOR ALL CURRENT VERSIONS
    def __init__(self, fname, lname, num, pos, str, spd, shot, img, uni, rink):
        self.fname, self.lname = fname, lname
        self.number, self.pos = num, pos
        self.str, self.spd, self.shot = str,spd,shot
        self.vx, self.vy = 0,0
        self.img = pygame.image.load("game/img/"+img).convert()
        self.img.set_colorkey((PUREGREEN))
        self.x,self.y = 0,0
        self.facing,self.flipped = "l",False
        self.uni, self.rink = uni, rink
        self.width, self.height = 0,0
        self.homeTeam, self.awayTeam = False, False
        
    # string to return when called upon
    def __str__(self):
        return self.fname + " " + self.lname
        
    # fetch and return rectangles for various parts of the player
    def getRect(self,bodyPart):
        u, img = self.uni, self.img.get_rect()
        if bodyPart == "body":
            if self.facing == "l":
                # body before scaling is Rect(690,230,610,1175)
                return pygame.Rect(self.x+(.4929*img.width), self.y+(.1036*img.height), img.width*.4357 , img.height*.8392 )
            elif self.facing == "r":
                # body before scaling is Rect(100,150,610,1175)
                return pygame.Rect(self.x+(.0714*img.width), self.y+(.1036*img.height), img.width*.4357 , img.height*.8392 )
        elif bodyPart == "full":
            if self.facing == "l":
                # full before scaling is Rect(35,145,1265,1175)
                return pygame.Rect(self.x+(.0243*img.width), self.y+(.1036*img.height), img.width*.9036, img.height*.8392 )
            elif self.facing == "r":
                # full before scaling is Rect(100,140,1265,1175)
                return pygame.Rect(self.x+(.0714*img.width), self.y+(.1000*img.height), img.width*.9036, img.height*.8392 )
        elif bodyPart == "stick":
            #stick size? .1379, .5
            if self.facing == "l":
                # stick before scaling is Rect(55,1160,207,70)
                return pygame.Rect(self.x+(.0393*img.width), self.y+(.8286*img.height), img.width*.18, img.height*.06)
            if self.facing == "r":
                # stick before scaling is Rect(1135,1155,207,70)
                return pygame.Rect(self.x+(.8107*img.width), self.y+(.8250*img.height), img.width*.18, img.height*.06)
            
    # function so that player does not leave top of rink
    def doesBorderExistUp(self, rink):
        ## Check for border only when puck is moving up
        ## return True if border exists
        ## return False if no border and movement is allowed
        m = self.getRect("stick")
        ## above variables are to simplify code
        
        # top left circle
        bTL = rink.borderList[rink.getIndex("ctl")].getRect()
        cTL = bTL.center
        distFromCenterTL = ((m.x-cTL[0])**2 + ((m.y-(m.height/2))-cTL[1])**2)**.5
        if m.x < bTL.x+bTL.width/2:                # puck is on correct side of ice
            if m.x < cTL[0] and (m.y-(m.height/2)) <= cTL[1]:       # puck is in correct quadrant
                if distFromCenterTL > (bTL.width/2):      # check if puck is on edge
                    return True
        
        # top right circle
        bTR = rink.borderList[rink.getIndex("ctr")].getRect()
        cTR = bTR.center
        distFromCenterTR = (((m.x+m.width)-cTR[0])**2 + (((m.y-(m.height/2)))-cTR[1])**2)**.5
        if m.x > bTR.x:                                 # puck is on correct side of ice
            if m.x+m.width >= cTR[0] and (m.y-(m.height/2))+m.height <= cTR[1]:   # puck is in correct quadrant
                if distFromCenterTR > (bTR.width/2):       # check if puck is on edge
                    return True
        
        # rect
        bU = rink.borderList[rink.getIndex('rm')].getRect()
        if (m.y-(m.height/2)) <= bU.y:         #check if y is on edge
            return True
                
        #if all else fails you can move, return False
        return False

    # function so that puck does not leave bottom of rink
    def doesBorderExistDown(self, rink):
        ## Check for border only when puck is moving down
        ## return True if border exists 
        ## return False if no border and movement is allowed
        m = self.getRect("stick")
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

    # function so that puck does not leave left of rink
    def doesBorderExistLeft(self, rink):
        ## Check for border only when puck is moving left
        ## return True if border exists
        ## return False if no border and movement is allowed
        m = self.getRect("stick")
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

    # function so that puck does not leave right of rink
    def doesBorderExistRight(self, rink):
        ## Check for border only when puck is moving right
        ## return True if border exists
        ## return False if no border and movement is allowed
        m = self.getRect("stick")
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
                
    # moves player based on manual input from player
    def moveManual(self,input):
        spd = getAdjustedValue(self.spd)
        horiz, vert = 0,0
        self.vx, self.vy = 0,0
        if input == "l" and not self.doesBorderExistLeft(self.rink):
            self.vx = abs(spd)*-1
            horiz = True
            self.facing = "l"
        if input == "r" and not self.doesBorderExistRight(self.rink):
            self.vx = abs(spd)
            horiz = True
            self.facing = "r"
        if input == "u" and not self.doesBorderExistUp(self.rink):
            self.vy = abs(spd)*-1
            vert = True
        if input == "d" and not self.doesBorderExistDown(self.rink):
            self.vy = abs(spd)
            vert = True
            
        # if player is moving vertically and horizontally, half each velocity
        # so that no speed advantage is gained
        if vert and horiz:
            self.vx = self.vx * 1/2
            self.vy = self.vy * 1/2
            
        # apply velocities to position
        self.x += getAdjustedValue(self.vx)
        self.y += getAdjustedValue(self.vy)
        
    # function for computer controlled player to move toward the puck
    def moveAuto(self,puck,rink):
        spd = getAdjustedValue(self.spd)
        horiz, vert = 0,0
#         self.vx, self.vy = 0,0
        if puck.x > 0:
            if puck.x+35 < self.getRect("stick").x-1 and not self.doesBorderExistLeft(self.rink):
                self.vx = abs(spd)*-1
                horiz = True
                self.facing = "l"
            elif puck.x-35 > self.getRect("stick").x+1 and not self.doesBorderExistRight(self.rink):
                self.vx = abs(spd)
                horiz = True
                self.facing = "r"
#             else:
#                 self.vx = 0
            if puck.y < self.getRect("stick").y and not self.doesBorderExistUp(self.rink):
                self.vy = abs(spd)*-1
                vert = True
            elif puck.y > self.getRect("stick").y and not self.doesBorderExistDown(self.rink):
                self.vy = abs(spd)
                vert = True
            else:
                self.vy = 0
                
        # if player is moving vertically and horizontally, half each velocity
        # so that no speed advantage is gained
        if vert and horiz:
            self.vx = self.vx * 1/2
            self.vy = self.vy * 1/2
            
        # apply velocities to position
        self.x += getAdjustedValue(self.vx)
        self.y += getAdjustedValue(self.vy)
        
    # handle puck collisions
    def collideWithPuck(self,puck):
        puckRect = pygame.Rect(puck.x,puck.y,puck.getRect().width,puck.getRect().height)
        if self.getRect("stick").colliderect(puckRect):
            # adjust strength of collision 
            strenY = abs(self.str) * -1 if self.vy < 0 else abs(self.str)
            strenX = abs(self.str) * -1 if self.vx < 0 else abs(self.str)
            if self.vx == 0:
                strenX = 0
            if self.vy == 0:
                strenY = 0
            # give puck velocity
            puck.vx += strenX
            puck.vy += strenY 
            puck.vxStored, puck.vyStored = puck.vx, puck.vy
            
    # update player info
    def update(self,screen,puck,auto,rink):
        # make sure player is facing the way he is skating
        if self.facing == "l" and self.flipped:
            self.img = pygame.transform.flip(self.img,1,0)
            self.flipped = False
        elif self.facing == "r" and not self.flipped:
            self.img = pygame.transform.flip(self.img,1,0)
            self.flipped = True
            
        # use for debugging of hitboxes
#         pygame.draw.rect(screen, (200,0,0), self.getRect("body"), 2)
#         pygame.draw.rect(screen, (0,0,200), self.getRect("stick"), 2)
#         pygame.draw.rect(screen, (0,200,0), self.getRect("full"), 2)

        # if computer controlled, move
        if auto:
            self.moveAuto(puck,rink)

        # check for puck collisions
        self.collideWithPuck(puck)
        
        # draw player on the screen - most important part!
        screen.blit(self.img, (self.x,self.y))
        