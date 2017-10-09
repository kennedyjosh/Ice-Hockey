import pygame
from constants import *

# this is the embodiment of the game, where all calculations occur
# and all info is displayed to the screen. This class brings all the other 
# game classes together
class Engine:
    # initialize
    def __init__(self, Rink, HomeTeam, AwayTeam, Puck, Scoreboard, userTeam):
        self.rink, self.home, self.away, self.puck, self.sb = Rink, HomeTeam, AwayTeam, Puck, Scoreboard
        if userTeam == self.home:
            # team.initialize(user, comp, away, home) # all True/False
            self.home.initialize(True,False,False,True)
            self.away.initialize(False,True,True,False)
        else:
            self.away.initialize(True,False,True,False)
            self.home.initialize(False,True,False,True)
            
    # on-screen notification of goal scored
    def goalNotification(self, screen, teamThatScored):
        if teamThatScored == self.home:
            msg = "Scored by "+str(teamThatScored.currentPlayer)+". Press the spacebar to continue."
            other = self.away
        else:
            msg = "Scored by "+str(teamThatScored.playerList[0])+". Press the spacebar to continue."
            other = self.home
        goalFont = pygame.font.Font(None, 85)
        infoFont = pygame.font.Font(None, 50)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        return
                    
            # place players at center ice faceoff dot
            for t in [teamThatScored,other]:
                for p in t.playerList:
                    u = p.uni
                    p.x, p.y = 0,0
                    if p.homeTeam:
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

                    
            screen.fill((0,0,0))
            self.rink.updatePartially(screen)
            
            screen.blit(goalFont.render("Goal!",1,teamThatScored.primaryColor),(W/2-goalFont.size("Goal!")[0]/2,H/2-100))
            screen.blit(infoFont.render(msg,1,teamThatScored.primaryColor),(W/2-infoFont.size(msg)[0]/2,H/2))
            
            pygame.display.flip()
            
    # function to check for win
    # currently, 3 goals is needed to win
    def checkForWin(self,screen):
        end = False
        if int(self.sb.hScore.textString) >= 3:
            # home team won
            end = self.displayWin(self.home,screen)
        elif int(self.sb.aScore.textString) >= 3:
            # away team won
            end = self.displayWin(self.away,screen)
        return end
    
    # if someone wins, display a message conveying that fact
    # and then return to the main menu
    def displayWin(self,winner,screen):
        msg = "The "+str(winner.name)+" won! Press the spacebar to continue."
        infoFont = pygame.font.Font(None, 84)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        return True
            
            self.rink.updatePartially(screen)
                    
            screen.blit(infoFont.render(msg,1,winner.primaryColor),(W/2-infoFont.size(msg)[0]/2,H/2-infoFont.size(msg)[1]/2))
            
            pygame.display.update()
        
    # update all the game classes
    def update(self,screen):
        # draw rink to screen
        loc, goal = self.rink.update(screen, self.puck)
        if goal:
            #goal has been scored
            self.puck.vx, self.puck.vy = 0,0
            self.puck.fricTrack = 0
            self.puck.vxStored, self.puck.vyStored = 0,0
            if loc == "l":
                self.sb.addScore("home")
                scorer = self.home
            else:
                self.sb.addScore("away")
                scorer = self.away
            self.goalNotification(screen,scorer)
                
        # check to see if someone won
        if self.checkForWin(screen):
            return True
        
        # draw goal lines:
        # this needs to be done after checking for win & goal because
        # for the background of the win/goal notifications I use an empty
        # arena template
        u = self.rink.boardsList[0].uni
        pygame.draw.line(screen, RED, (u.rx + 2*(11*u.c),u.ry),(u.rx + 2*(11*u.c),u.ry+u.width), int(u.c))
        pygame.draw.line(screen, RED, (u.rx+(u.len+(28*u.c)) - 2*(11*u.c),u.ry),(u.rx+(u.len+(28*u.c)) - 2*(11*u.c),u.ry+u.width), int(u.c))

        # update scoreboard
        self.sb.update(screen)
                    
        # update teams
        self.home.update(screen,self.puck,self.rink)
        self.away.update(screen,self.puck,self.rink)
        
        # temporary center ice marker
        pygame.draw.rect(screen, (200,0,0), (self.rink.borderList[self.rink.getIndex("rm")].getRect().center[0]-2.5,self.rink.borderList[self.rink.getIndex("rm")].getRect().center[1]-2.5,5,5), 2)
            
        # update puck
        self.puck.update(screen,self.rink)            
        
        if goal:
            for team in [self.home, self.away]:
                team.startPos(self.puck,screen)

            
