import pygame

def writeText(font,text,size,color,position,screen):
    screen.blit(font.render(text,1,color),position)

## A Button that can be clicked. Class also handles text placement and setup
## for ease of use to user
class Button:
    ## Initialize 
    def __init__(self,locationTuple,width, height, text, color, customFont = None):
        self.x, self.y = locationTuple[0], locationTuple[1]
        self.width, self.height = width, height
        self.textString, self.textColor = text, (255,255,255)
        self.textPos, self.textSize = "C", 45
        self.textFont = pygame.font.Font(customFont, self.textSize)
        self.colorR, self.colorG, self.colorB = color[0],color[1],color[2]
        self.storedColorR, self.storedColorG, self.storedColorB = color[0],color[1],color[2]
        self.clicking,self.enabled = False,True
        
    def __str__(self):
        return "[Button @ ("+str(self.x)+","+str(self.y)+")]"
        
    ## Return a pygame rect
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)
    
    ## Return a tuple containing the color of the button
    def getColor(self):
        return (self.colorR, self.colorG, self.colorB)
    
    def setColor(self,r,g,b):
        self.colorR = r 
        self.colorG = g 
        self.colorB = b 
    
    ## Find where in the button text should be placed
    ## self.textPos should be: TL, TC, TR, L, C, R, BL, BC, BR
    def getTextPos(self):
        pos = [0,0]
        if self.textPos.endswith("L"):
            pos[0] = self.getRect().x 
            pos[1] = (self.getRect().y+self.getRect().height/2)-(self.textFont.size(self.textString)[1]/2)
        elif self.textPos.endswith("C"):
            pos[0] = (self.getRect().x+self.getRect().width/2)-(self.textFont.size(self.textString)[0]/2)
        elif self.textPos.endswith("R"):
            pos[0] = self.getRect().x+self.getRect().width-(self.textFont.size(self.textString)[0])
            pos[1] = (self.getRect().y+self.getRect().height/2)-(self.textFont.size(self.textString)[1]/2)
        if self.textPos.startswith("T"):
            pos[1] = self.getRect().y
        elif self.textPos.startswith("B"):
            pos[1] = self.getRect().y+self.getRect().height-(self.textFont.size(self.textString)[1])
        if self.textPos == "C":
            pos[0] = (self.getRect().x+self.getRect().width/2)-(self.textFont.size(self.textString)[0]/2)
            pos[1] = (self.getRect().y+self.getRect().height/2)-(self.textFont.size(self.textString)[1]/2)
        if self.textPos not in ["TL","TC","TR","L","C","R","BL","BC","BR"]:
            raise Exception("Invalid textPos for button: "+str(self)+"\n\tPlease use: TL,TC,TR,L,C,R,BL,BC,BR")
        return (pos[0],pos[1])
            
    ## Make button appear darker while being clicked
    def isBeingClicked(self):
        if self.enabled:
            self.storedColorR, self.storedColorG, self.storedColorB = self.colorR, self.colorG, self.colorB
            for _ in range(20):
                self.colorR -= 1 if self.colorR > 0 else 0
                self.colorG -= 1 if self.colorG > 0 else 0
                self.colorB -= 1 if self.colorB > 0 else 0
            self.clicking = True
            
    ## Make button appear as normal after darkening during click
    def isDoneBeingClicked(self):
        if self.enabled:
            for _ in range(20):
                self.colorR += 1 if self.colorR < self.storedColorR and self.colorR < 255 else 0
                self.colorG += 1 if self.colorG < self.storedColorG and self.colorG < 255 else 0
                self.colorB += 1 if self.colorB < self.storedColorB and self.colorB < 255 else 0
            self.clicking = False
            
    ## Draw button to screen
    def draw(self,screen):
        if self.enabled:
            try:
                pygame.draw.rect(screen, self.getColor(), self.getRect())
            except:
                for i,c in enumerate([self.colorR, self.colorB, self.colorG]):
                    while c < 0:
                        c += 2
                    while c > 255:
                        c -= 2
                    if i == 0:
                        self.setColor(c,self.colorG,self.colorB)
                    elif i == 1:
                        self.setColor(self.colorR,c,self.colorB)
                    else:
                        self.setColor(self.colorR, self.colorG, c)
                pygame.draw.rect(screen, (abs(self.colorR), abs(self.colorB), abs(self.colorG)), self.getRect())
                
            writeText(self.textFont,self.textString,self.textSize,self.textColor,self.getTextPos(),screen)
        
## Acts a bit like a button, but not click-able
class Label:
    ## Initialize
    def __init__(self,locationTuple,width, height, text, customFont = None):
        self.x, self.y = locationTuple[0], locationTuple[1]
        self.width, self.height = width, height
        self.textString, self.textColor = text, (255,255,255)
        self.textPos, self.textSize = "C", 30
        self.customFont = customFont
        self.textFont = pygame.font.Font(customFont, self.textSize)
        
    def __str__(self):
        return "[Label @ ("+str(self.x)+","+str(self.y)+")]"
        
    ## Return a pygame rect
    def getRect(self):
        return pygame.Rect(self.x,self.y,self.width,self.height)
        
    ## Find where in the label text should be placed
    ## self.textPos should be: TL, TC, TR, L, C, R, BL, BC, BR
    def getTextPos(self):
        pos = [0,0]
        if self.textPos.endswith("L"):
            pos[0] = self.getRect().x 
            pos[1] = (self.getRect().y+self.getRect().height/2)-(self.textFont.size(self.textString)[1]/2)
        elif self.textPos.endswith("C"):
            pos[0] = (self.getRect().x+self.getRect().width/2)-(self.textFont.size(self.textString)[0]/2)
        elif self.textPos.endswith("R"):
            pos[0] = self.getRect().x+self.getRect().width-(self.textFont.size(self.textString)[0])
            pos[1] = (self.getRect().y+self.getRect().height/2)-(self.textFont.size(self.textString)[1]/2)
        if self.textPos.startswith("T"):
            pos[1] = self.getRect().y
        elif self.textPos.startswith("B"):
            pos[1] = self.getRect().y+self.getRect().height-(self.textFont.size(self.textString)[1])
        if self.textPos == "C":
            pos[0] = (self.getRect().x+self.getRect().width/2)-(self.textFont.size(self.textString)[0]/2)
            pos[1] = (self.getRect().y+self.getRect().height/2)-(self.textFont.size(self.textString)[1]/2)
        if self.textPos not in ["TL","TC","TR","L","C","R","BL","BC","BR"]:
            raise Exception("Invalid textPos for label: "+str(self)+"\n\tPlease use: TL,TC,TR,L,C,R,BL,BC,BR")
        return (pos[0],pos[1])
    
    ## Determine what size the text should be
    def setTextSize(self):
        w,h = self.getRect().width, self.getRect().height
        while self.textFont.size(self.textString)[0] > w and self.textFont.size(self.textString)[1] < h and self.textSize > 5:
            self.textSize -= 1
            self.textFont = pygame.font.Font(self.customFont, self.textSize)
        
    ## Draw button to screen
    def draw(self,screen):
        self.setTextSize()
        writeText(self.textFont,self.textString,self.textSize,self.textColor,self.getTextPos(),screen)

    
    
    
    
    
        
        