import pygame
from structure import *

def mainRules(opt):
    W,H = 1440, 900
    screen = opt[8]
    # used imported data to determine button color
    if opt[0]:
        #gradient
        gradient = True
        color = (opt[2],0,opt[1])
    elif opt[1] == 240:
        # red
        gradient = False
        color = (240,0,0)
    else:
        #blue
        gradient = False
        color = (0,0,240)
        
    # set up exit button to return to main menu
    exitBtn = Button((W/2-150,H-125),300,75,"Back", color)
    exitBtn.textColor = (255,255,255)
    buttons = [exitBtn]
    
    # set up label to display text
    lblText = (
        "Objective: Score 3 goals by putting the puck into your opponents net.\nYou will lose if you allow 3 goals to be scored against you.\n\nControls: Use WASD or the arrow keys to move."
        )
    lbl = Label((25,25),W-50, H-150, lblText)
    lbl.textColor = (0,0,0)
    lbl.textPos = "TC"
    
    # from imported data, setup the background image
    bg, bgRect = opt[3], opt[4]
    delay, movingDown, decr = opt[5], opt[6], opt[7]
    
    
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
                if mouse.colliderect(exitBtn.getRect()):
                    return [True,gradient, exitBtn.colorR, exitBtn.colorB, bg, bgRect, delay, movingDown, decr, screen]

                
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
            if exitBtn.colorR <= 0:
                decr = False
            elif exitBtn.colorR >= 235:
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
            
        lbl.draw(screen)
        
        pygame.display.flip()

                
                








