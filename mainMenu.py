import sys, main
 
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 840, 580
gameDisplay = pygame.display.set_mode((width, height))
font_20 = pygame.font.Font("IBMPlexSans-Regular.ttf", 20)
font_60 = pygame.font.Font("IBMPlexSans-Regular.ttf", 60)
 
def MainMenu():

    game_run = True
    while game_run:
        gameDisplay.fill((0, 150, 0))
        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        gameDisplay.blit(font_60.render("Block Tower Defense", True, (0, 0, 0)), (130, 150))

        for event in pygame.event.get():
            if event.type == QUIT:
              pygame.quit()
              sys.exit()

        pygame.draw.rect(gameDisplay, (150, 0, 0), (340, 320, 150, 75), 0)
        pygame.draw.rect(gameDisplay, (100, 0, 0), (340, 320, 150, 75), 2)
        gameDisplay.blit(font_20.render("New Game", True, (0, 0, 0)), (365, 350))
        if 340 <= pos[0] <= 490 and 320 <= pos[1] <= 395 and pressed[0] == 1:
            main.game_loop(False)

        pygame.draw.rect(gameDisplay, (150, 0, 0), (150, 320, 150, 75), 0)
        pygame.draw.rect(gameDisplay, (100, 0, 0), (150, 320, 150, 75), 2)
        gameDisplay.blit(font_20.render("Continue", True, (0, 0, 0)), (180, 350))
        if 150 <= pos[0] <= 300 and 320 <= pos[1] <= 395 and pressed[0] == 1:
            main.game_loop(True)

        pygame.draw.rect(gameDisplay, (150, 0, 0), (530, 320, 150, 75), 0)
        pygame.draw.rect(gameDisplay, (100, 0, 0), (530, 320, 150, 75), 2)
        gameDisplay.blit(font_20.render("Nothing Yet", True, (0, 0, 0)), (550, 350))
        

        pygame.display.flip()
        fpsClock.tick(fps)

if __name__ == "__main__":
    MainMenu()
