# import required modules
import pygame,sys,cursor,os,random
from structure import *
from __builtin__ import False

# main function
def main(opt):
    # initialize everything if not already done
    if opt[0] == False:
        #initialize window, basic setup stuff
        pygame.init()
        screen = None
        W,H = 1440, 900
        if os.name == 'nt': #windows stuff
            screen = pygame.display.set_mode((W,H),pygame.FULLSCREEN)
        else: # mac stuff
            screen = pygame.display.set_mode((W,H))
        
        # set up cursor, buttons, and images
        cursor.getCursor("black")
    
        # decide what color the buttons will be
        color = random.randint(0,3)
        if color == 1:
            gradient = True
            color = (235,0,0)
        elif color == 2:
            gradient = False
            color = (240,0,0)
        else:
            gradient = False
            color = (0,0,240)
        # background image
        bg = pygame.image.load("menu/img/rinkbg.png").convert()
        bgRect = pygame.Rect(-1287,-274,1440,900)
        movingDown, decr = True, True
        delay = 0
    # if initialization is done, carry those variables back for a smooth transition
    else:
        W,H = 1440, 900
        screen = opt[9]
        # used imported data to determine button color
        if opt[1]:
            #gradient
            gradient = True
            color = (opt[3],0,opt[2])
        elif opt[2] == 240:
            # red
            gradient = False
            color = (240,0,0)
        else:
            #blue
            gradient = False
            color = (0,0,240)
            
        # from imported data, setup the background image
        bg, bgRect = opt[4], opt[5]
        delay, movingDown, decr = opt[6], opt[7], opt[8]
            

    startBtnText = "Play"
    startBtn = Button((W/2-150,H/2-90),300,75,startBtnText, color)
    startBtn.textColor = (255,255,255)
    
    rulesBtnText = "Rules"
    rulesBtn = Button((W/2-150,H/2),300,75,rulesBtnText, color)
    rulesBtn.textColor = (255,255,255)
    
    quitBtnText = "Quit"
    quitBtn = Button((W/2-150,H/2+90),300,75,quitBtnText, color)
    quitBtn.textColor = (255,255,255)
    
    #list to hold all the buttons
    buttons = [startBtn, rulesBtn, quitBtn]
    

    
    ##############################    MAIN LOOP
    while True:
        mouse = pygame.mouse.get_pos()
        mouse = pygame.Rect(mouse[0],mouse[1],1,1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() 
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_f:
                    pass
            elif event.type == pygame.MOUSEMOTION:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if mouse.colliderect(button.getRect()):
                        button.isBeingClicked()
            elif event.type == pygame.MOUSEBUTTONUP:
                # action will only happen once button is done being clicked
                # and the mouse is still on that button
                for button in buttons:
                    if button.clicking:
                        button.isDoneBeingClicked()
                if mouse.colliderect(startBtn.getRect()):
                    pygame.mouse.set_visible(0)
                    return "start", [False]
                if mouse.colliderect(rulesBtn.getRect()):
                    return "rules", [gradient, startBtn.colorR, startBtn.colorB, bg, bgRect, delay, movingDown, decr, screen]
                elif mouse.colliderect(quitBtn.getRect()):
                    return "quit", [False]
                
        if gradient:
        # button gradient  handling (if present)
            for b in buttons:
                if abs(b.colorR-b.colorB) > 170:
                    if decr == True:
                        b.colorB += .5
                        b.colorR -= .5
                        b.storedColorB += .5
                        b.storedColorR -= .5
                    else:
                        b.colorB -= .5
                        b.colorR += .5
                        b.storedColorB -= .5
                        b.storedColorR += .5
                else:
                    if decr == True:
                        b.colorB += 1.25
                        b.colorR -= 1.25
                        b.storedColorB += 1.25
                        b.storedColorR -= 1.25
                    else:
                        b.colorB -= 1.25
                        b.colorR += 1.25
                        b.storedColorB -= 1.25
                        b.storedColorR += 1.25          
            if startBtn.colorR <= 0:
                decr = False
            elif startBtn.colorR >= 235:
                decr = True
        
          
        # handle movement of background  
        if delay == 3:    
            if movingDown:
                bgRect.x += 1
                bgRect.y -= 2
            else:
                bgRect.x -= 1
                bgRect.y += 2
                
            if bgRect.x >= -700:
                movingDown = False
            elif bgRect.x <= -1287:
                movingDown = True
            delay = 0
        delay += 1
        
        
        
        # refresh the screen
        screen.blit(bg, (bgRect.x,bgRect.y))
        
        # draw all the buttons
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()


# this file WILL run if launched directly but it is NOT recommended
# none of the buttons will work except for quit if run as __main__
if __name__ == "__main__":
    main()