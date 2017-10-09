import pygame
from structure import *

# class to hold the score and display this information
class Scoreboard:
    # initialize
    def __init__(self, home, away, position, w, h):
        # create shorthand
        fromLeft,fromRight = position[0],position[0]+w
        # initialize team logos
        self.hBGcolor, self.aBGcolor = home.primaryColor, away.primaryColor
        self.hLogo, self.hLogoRect = home.logo, pygame.Rect(fromLeft,position[1],w*.3125,h*.75)
        self.aLogo, self.aLogoRect = away.logo, pygame.Rect(fromRight-w*.3125,position[1],w*.3125,h*.75)
        self.hLogo = pygame.transform.scale(self.hLogo,(self.hLogoRect.width,self.hLogoRect.height))
        self.aLogo = pygame.transform.scale(self.aLogo,(self.aLogoRect.width,self.aLogoRect.height))
        # initialize labels to hold team names and scores
        self.hName = Label((fromLeft,position[1]+h*.75),w*.3125,h*.25,home.city+" "+home.name)
        self.aName = Label((fromRight-w*.3125,position[1]+h*.75),w*.3125,h*.25,away.city+" "+away.name)
        self.aScore = Label((fromLeft+w*.3125,position[1]),w*.1875,h,"0")
        self.hScore = Label((fromRight-w*(.3125+.1875),position[1]),w*.1875,h,"0")
        self.labels = [self.hName, self.aName, self.hScore, self.aScore]
        # put the scoreboard somewhere on the Surface
        self.x, self.y = position[0], position[1]
        self.width, self.height = w, h
        # some optimizing of font size for score display 
        self.hScore.textSize = 110
        self.aScore.textSize = 110
        self.hScore.textFont = pygame.font.Font(self.hScore.customFont, self.hScore.textSize)
        self.aScore.textFont = pygame.font.Font(self.aScore.customFont, self.aScore.textSize)
     
    # add one point to a team           
    def addScore(self,homeORaway):
        if homeORaway == "home":
            self.hScore.textString = str(int(self.hScore.textString) + 1)
        else:
            self.aScore.textString = str(int(self.aScore.textString) + 1)
       
    # update scoreboard info     
    def update(self, screen):
        #background of scoreboard
        pygame.draw.rect(screen, (0,0,0),(self.x,self.y,self.width,self.height))
        
        # information
        for lbl in self.labels:
            lbl.draw(screen)
        # i didnt like these so i left them out, I didnt think they looked good
#         pygame.draw.rect(screen, self.hBGcolor, self.hLogoRect)
#         pygame.draw.rect(screen, self.aBGcolor, self.aLogoRect)
        screen.blit(self.hLogo, (self.hLogoRect.x, self.hLogoRect.y))
        screen.blit(self.aLogo, (self.aLogoRect.x, self.aLogoRect.y))
        
        #outline of scoreboard
        pygame.draw.rect(screen, (255,200,0),(self.x-2,self.y-2,self.width+4,self.height+4),4)

            
