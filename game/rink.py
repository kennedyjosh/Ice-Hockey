import pygame
from constants import *

# class to hold the rink together and manage all parts of the rink, most
# of which are purely decorative, but some serve a purpose
class Rink:
    # initialize
    def __init__(self, borderList, insideList, boardsList, NetList):
        self.borderList = borderList
        self.insideList = insideList
        self.boardsList = boardsList
        self.netList = NetList
        
    # return the location of an object
    def getLoc(self,obj):
        try:
            obj.getRect()
        except:
            print "No Rect"
            
        for item in self.borderList:
            if not item.shape == "r":
                if obj.getRect().colliderect(item.getRect()):
                    return item
        return self.borderList[self.getIndex('rm')]
            
    # return the index of a particular rink function from its list
    def getIndex(self, st):
        for t in range(len(self.borderList)):
            if st == self.borderList[t].shape+self.borderList[t].loc:
                return int(t)
    
    # return the rect of the net requested
    def getNet(self,net):
        if net == "r":
            for n in self.netList:
                if n.loc == "r":
                    return n.getRect()
        else:
            for n in self.netList:
                if n.loc == "l":
                    return n.getRect()
            
    # only update visible parts of rink, not nets or lines
    def updatePartially(self, screen):
        # border does not visibly show so you can include it or not
        for b in self.borderList:
            b.update(screen)
        for d in self.boardsList:
            d.update(screen, self)
        for i in self.insideList:
            i.update(screen, self)

    # update entire rink and return a bool for goal scored
    def update(self, screen, puck):
        # border does not visibly show so you can include it or not
        for b in self.borderList:
            b.update(screen)
        for d in self.boardsList:
            d.update(screen, self)
        for i in self.insideList:
            i.update(screen, self)
        for n in self.netList:
            if n.update(screen,puck):
                return n.loc,True
        return "",False

# class to hold border shapes of rink, very important for collisions
class Border():
    # initialize
    def __init__(self,shape,location,color,universal):
        ## shape should be 'c' or 'r'
        ## location should be two letters: 't'/'b' for top or bottom, 'l'/'r' for left or right
        ## or location should be one letter, 'l'/'m'/'r'
        self.shape, self.loc = shape, location
        self.uni = universal
        self.color = color
    
    # return string carrying information about itself
    def __str__(self):
        return str(self.shape)+str(self.loc)
    
    # get bounding rectangle of shape    
    def getRect(self):
        # shortcut
        u = self.uni
        # anything on the right, x direction code
        xr = u.rx + (172 * u.c)
        # circle on the bottom, y direction code
        ybc = u.ry + (29 * u.c)
        
        if self.shape == "c":
            if self.loc.startswith("t"):
                if self.loc.endswith("l"):
                    # top left circle
                    return pygame.Rect( u.rx , u.ry, u.cornerDia, u.cornerDia )
                else:
                    # top right circle
                    return pygame.Rect( xr, u.ry, u.cornerDia, u.cornerDia )
            else:
                if self.loc.endswith("l"):
                    # bottom left circle
                    return pygame.Rect( u.rx, ybc, u.cornerDia, u.cornerDia )
                else:
                    # bottom right circle
                    return pygame.Rect( xr, ybc, u.cornerDia, u.cornerDia)
        else:
            # huge rect
            return pygame.Rect( u.rx, u.ry, (228 * u.c), (85 * u.c))
          
    # draw the border to the screen, not really necessary    
    def update(self,screen):
        if self.shape == "c":
            pygame.draw.ellipse(screen, self.color, self.getRect(), 1)
        else:
            pygame.draw.rect(screen, self.color, self.getRect(), 1)

# class to hold all the shapes that will need to visually show the rink
class Inside():
    # initialize
    def __init__(self,shape,location,color,borderList,offset, universal):     
        ## shape should be 'c' or 'r'
        ## location should be two letters: 't'/'b' for top or bottom, 'l'/'r' for left or right
        ## or location should be one letter, 'l'/'m'/'r'
        self.shape, self.loc = shape, location
        self.color, self.offset = color, offset
        self.borderList = borderList
        self.uni = universal
           
    # get bounding rectangle for shape
    def getRect(self,rink):
        # shortcuts
        u,o = self.uni, self.offset
        # anything on the right, x direction code
        xr = u.rx + (172 * u.c)
        # circle on the bottom, y direction code
        ybc = u.ry + (29 * u.c)
        # side rect size
        srs = (28*u.c)
        
        if self.shape == "c":
            if self.loc.startswith("t"):
                if self.loc.endswith("l"):
                    # top left circle
                    return pygame.Rect( u.rx-o, u.ry-o, u.cornerDia+2*o, u.cornerDia+2*o )
                else:
                    # top right circle
                    return pygame.Rect( xr-o, u.ry-o, u.cornerDia+2*o, u.cornerDia+2*o )
            else:
                if self.loc.endswith("l"):
                    # bottom left circle
                    return pygame.Rect( u.rx-o, ybc-o, u.cornerDia+2*o, u.cornerDia+2*o )
                else:
                    # bottom right circle
                    return pygame.Rect( xr-o, ybc-o, u.cornerDia+2*o, u.cornerDia+2*o )
        else:
            if self.loc == "m":
                # huge rect (middle)
                return pygame.Rect( u.rx+(28*u.c)-o, u.ry-o, (172*u.c)+2*o, (85*u.c)+2*o )
            elif self.loc == "l":
                # left rect
                return pygame.Rect( u.rx-o, u.ry+srs-o, srs+2*o, srs+2*o )
            else:
                # right rect
                return pygame.Rect( u.rx+(200*u.c)-o, u.ry+srs-o, srs+2*o, srs+2*o)
            
    # draw to screen
    def update(self,screen,rink):
        if self.shape == "c":
            pygame.draw.ellipse(screen, self.color, self.getRect(rink))
        else:
            pygame.draw.rect(screen, self.color, self.getRect(rink))

# class to hold the two nets
class Net():
    # initialize
    def __init__(self,loc,uni):
        self.loc = loc 
        self.uni = uni
        
    # returns rectangle of net
    def getRect(self):
        # simplify universal variable as u
        u = self.uni
        # define width and height of net
        width = 6 * u.c 
        height = 10 * u.c

        # find position of net
        if self.loc == "l":
            x = u.rx + 2*(11 * u.c)
            y = u.ry + (u.width/2 - height/2)
            x -= width
        else:
            x = u.rx + (u.len+(28*u.c)) - 2*(11*u.c)
            y = u.ry + (u.width/2 - height/2)
            
        return pygame.Rect(x,y,width,height)
    
    # checks if a goal has been scored
    def checkForGoal(self,puck):
        puckRect = pygame.Rect(puck.x,puck.y,puck.getRect().width,puck.getRect().height)
        if puckRect.colliderect(self.getRect()):
            if self.loc == "l":
                if puck.vx < 0:
                    return True
                elif puck.vx > 0:
                    puck.vx *= -1
                else:
                    puck.vy *= -1
            else:
                if puck.vx > 0:
                    return True
                elif puck.vx < 0:
                    puck.vx *= -1
                else:
                    puck.vy *= -1
        return False
    
    # draw to screen and return if goal has been scored
    def update(self,screen,puck):
        pygame.draw.rect(screen, RED, self.getRect(), int(self.uni.c/2))
        return self.checkForGoal(puck)
        
        
        
        