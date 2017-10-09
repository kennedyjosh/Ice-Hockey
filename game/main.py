'''
Josh Kennedy
----------------------------------
Honors Intro to Video Game Design Final Project 
"Hockey 2017"
----------------------------------
V ALPHA 3.2
'''
# import modules and stuff from supporting files
import pygame, math, time, sys, os
from rink import *
from gameEngine import *
from constants import *
from puck import *
from players import *
from scoreboard import *


def main(rinkScale = 6):
    
    #initialize window, basic setup stuff
    pygame.init()
    screen = None
    if os.name == 'nt': #windows stuff
        screen = pygame.display.set_mode((W,H),pygame.FULLSCREEN)
    else: # mac stuff
        screen = pygame.display.set_mode((W,H))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Ice Hockey")
    
    #universal variables, in a class I suppose
    scale = rinkScale   #change this to change size of rink, should be 6 for normal use
    uni = Universal(scale, ( W/2 - (114*scale) , H/2 - (42.5 * scale) ))
    
    #create border of rink
    b1, b2 = Border("c","tl",BLACK,uni), Border("c","tr",BLACK,uni)
    b3, b4 = Border("c","bl",BLACK,uni), Border("c","br",BLACK,uni)
    b5 = Border("r","m",BLACK,uni)
    borderList = [b5,b4,b2,b1,b3]
    
    #fill rink to make it look like it should
    i1, i2 = Inside("c","tl",WHITE,borderList,2,uni), Inside("c","tr",WHITE,borderList,2,uni)
    i3, i4 = Inside("c","bl",WHITE,borderList,2,uni), Inside("c","br",WHITE,borderList,2,uni)
    i5, i6, i7 = Inside("r","l",WHITE,borderList,2,uni),Inside("r","m",WHITE,borderList,2,uni),Inside("r","r",WHITE,borderList,2,uni)
    insideList = [i6,i5,i7,i4,i2,i1,i3]
    
    offset = int(2.5 * uni.c)
    #create more inside shapes and make them bigger to be the boards
    d1, d2 = Inside("c","tl",YELLOW,borderList,offset,uni), Inside("c","tr",YELLOW,borderList,offset,uni)
    d3, d4 = Inside("c","bl",YELLOW,borderList,offset,uni), Inside("c","br",YELLOW,borderList,offset,uni)
    d5, d6, d7 = Inside("r","l",YELLOW,borderList,offset,uni),Inside("r","m",YELLOW,borderList,offset,uni),Inside("r","r",YELLOW,borderList,offset,uni)
    boardsList = [d6,d5,d7,d4,d2,d1,d3]
    
    # create nets. this will never change
    nets = [Net("l",uni),Net("r",uni)]
    
    #set up the rink class
    rink = Rink(borderList,insideList,boardsList,nets)
    
    # create puck
    if __name__ == "__main__":
        pimg = pygame.transform.scale(pygame.image.load("img/puck.png").convert(), (int(1*uni.c),int(5*uni.c/6)))
    else:
        pimg = pygame.transform.scale(pygame.image.load("game/img/puck.png").convert(), (int(1*uni.c),int(5*uni.c/6)))
    pimg.set_colorkey((WHITE))
    pimg.get_rect().x = W/2
    pimg.get_rect().y = H/2
    puck = Puck(pimg,pimg.get_rect().width,pimg.get_rect().height)
    
    # create teams
    #optimaztions for mac or pc
    if os.name == "nt":
        str,spd,sh = 15,15,50
    else:
        str,spd,sh = 5,2,50
    
    ## Providence Eagles
        #joe lopez
    jLopezImg = "eaglesPlyr0.png"
    jLopez = Player("Joe", "Lopez", "9", "C", str,spd,sh, jLopezImg,uni,rink)
        #team setup
    eaglesPlyrList = [jLopez]
    eagleLogo = pygame.image.load("game/img/eagle-800px.png").convert()
    eagleLogo.set_colorkey((0,0,0))
    eagles = Team("Eagles", "Providence", "PRV", eagleLogo, YELLOW, BLACK, eaglesPlyrList, uni)
    
    ## Richmond Tigers
        #brendan clarke
    bClarkeImg = "tigersPlyr0.png"
    bClarke = Player("Brendan","Clarke","00","C",str,spd,sh,bClarkeImg,uni,rink)
        #team setup
    tigersPlyrList = [bClarke]
    tigersLogo = pygame.image.load("game/img/tiger.png").convert()
    tigers = Team("Tigers","Richmond","RCH",tigersLogo,ORANGE,BLACK,tigersPlyrList,uni)
    
    # create scoreboard/score keeping device
    sb = Scoreboard(eagles,tigers,(W/2-W*.25,25),W*.5,H*.15)
    
    userTeam = tigers
    #set up the game engine
    game = Engine(rink,tigers,eagles,puck,sb,userTeam)
    
    ##############################    MAIN LOOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
#                     print 1.0/getTickVal()
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_f:
                    game.away.startPos(game.puck, screen)
                    
        
        # control user movement
        p = pygame.key.get_pressed()
        if p[pygame.K_w] or p[pygame.K_UP]:
            userTeam.currentPlayer.moveManual("u")
        if p[pygame.K_s] or p[pygame.K_DOWN]:
            userTeam.currentPlayer.moveManual("d")
        if p[pygame.K_a] or p[pygame.K_LEFT]:
            userTeam.currentPlayer.moveManual("l")
        if p[pygame.K_d] or p[pygame.K_RIGHT]:
            userTeam.currentPlayer.moveManual("r")
    
        
        # Update screen                                     
        screen.fill(BLACK)
        
        # control framerate
        updateTickVal(clock.tick() / 1000.0)
        
        # update game
        # if game.update returns True, will return to the main menu
        if game.update(screen):
            pygame.mouse.set_visible(True)
            return
        
        pygame.display.flip()
        
# this file WILL run if launched directly but it is NOT recommended
if __name__ == "__main__":
    main()