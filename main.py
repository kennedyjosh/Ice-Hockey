'''
Hockey Game in Python using Pygame

by: Josh Kennedy
I can be reached by email at: jkennedy@suffolk.edu

This version was released on May 2017
'''
import sys, game, menu

def main():
    # holder variables for optional data to include between menus
    opt = [False]
    while True:
        # response holds the answer to what button the user clicked
        response, opt = menu.main(opt)
        
        # quit button
        if response == "quit":
            # ends application
            sys.exit()
            
        # start button
        elif response == "start":
            # launches game
            game.main()
            
        # rules button
        elif response == "rules":
            # show rules page
            opt = menu.mainRules(opt)
        
    
    
    
# This is the file you want to run if you want everything to work correctly! Have fun!
if __name__ == "__main__":
    main()