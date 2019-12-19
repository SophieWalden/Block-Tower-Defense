import sys, main, os
 
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 840, 580
gameDisplay = pygame.display.set_mode((width, height))
font_20 = pygame.font.Font("IBMPlexSans-Regular.ttf", 20)
font_30 = pygame.font.Font("IBMPlexSans-Regular.ttf", 30)
font_60 = pygame.font.Font("IBMPlexSans-Regular.ttf", 60)

def load_images(path_to_directory):
    """Loads all images"""
    images = {}
    for dirpath, dirnames, filenames in os.walk(path_to_directory):
        for name in filenames:
            if name.endswith('.png'):
                key = name[:-4]
                img = pygame.image.load(os.path.join(dirpath, name)).convert_alpha()
                images[key] = img
    return images
 
def MainMenu():

    Images = load_images("Images")
    game_run = True
    screen = "Main"
    step = 0
    cooldown = False
    Names = [["Classic", "Twisty Towers"]]
    SaveNames = ["Default", "Twisty"]
    Diff = ["Easy", "Medium", "Hard"]
    file = open("SaveFile/saveFile.txt", "r")
    data = file.readline().split("#")
    if len(data) != 4:
        data = ["0", "Medium", "0", "Medium"]
    
    while game_run:
        gameDisplay.fill((0, 150, 0))
        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == QUIT:
              pygame.quit()
              sys.exit()

        if screen == "Main":
            gameDisplay.blit(font_60.render("Block Tower Defense", True, (0, 0, 0)), (130, 150))

            pygame.draw.rect(gameDisplay, (150, 0, 0), (340, 320, 150, 75), 0)
            pygame.draw.rect(gameDisplay, (100, 0, 0), (340, 320, 150, 75), 2)
            gameDisplay.blit(font_20.render("New Game", True, (0, 0, 0)), (365, 350))
            if 340 <= pos[0] <= 490 and 320 <= pos[1] <= 395 and pressed[0] == 1:
                screen = "Map Select"
                cooldown = True

            pygame.draw.rect(gameDisplay, (150, 0, 0), (150, 320, 150, 75), 0)
            pygame.draw.rect(gameDisplay, (100, 0, 0), (150, 320, 150, 75), 2)
            gameDisplay.blit(font_20.render("Nothing Yet", True, (0, 0, 0)), (170, 350))
            if 150 <= pos[0] <= 300 and 320 <= pos[1] <= 395 and pressed[0] == 1:
                main.game_loop(True, "")

            pygame.draw.rect(gameDisplay, (150, 0, 0), (530, 320, 150, 75), 0)
            pygame.draw.rect(gameDisplay, (100, 0, 0), (530, 320, 150, 75), 2)
            gameDisplay.blit(font_20.render("Nothing Yet", True, (0, 0, 0)), (550, 350))

        elif screen == "Map Select":

            if step == 0:
                gameDisplay.blit(pygame.transform.scale(Images["Meadows"], (200, 150)), (100, 100))
                gameDisplay.blit(pygame.transform.scale(Images["TwistyTowers"], (200, 150)), (350, 100))
                if 100 <= pos[0] <= 300 and 100 <= pos[1] <= 250 and pressed[0] == 1 and not cooldown:
                    screen = "Dif Select"
                    Map = "Classic"
                    MapName = "Default"
                if 350 <= pos[0] <= 550 and 100 <= pos[1] <= 250 and pressed[0] == 1 and not cooldown:
                    screen = "Dif Select"
                    Map = "Twisty Towers"
                    MapName = "Twisty"
                    
 
            for i in range(2):
                pygame.draw.rect(gameDisplay, (100, 100, 100), (100+250*i, 100, 200, 150), 2)
                gameDisplay.blit(font_20.render(Names[step][i], True, (0, 0, 0)), (200+250*i-int(font_20.size(Names[step][i])[0]/2), 70))
                
            if pressed[0] == 0:
                cooldown = False


            pygame.draw.rect(gameDisplay, (100, 0, 0), (10, 10, 100, 75), 0)
            pygame.draw.rect(gameDisplay, (200, 0, 0), (10, 10, 100, 75), 3)
            gameDisplay.blit(font_30.render("Back", True, (0, 0, 0)), (25, 20))
            if 10 <= pos[0] <= 110 and 10 <= pos[1] <= 85 and pressed[0] == 1 and not cooldown:
                screen = "Main"
                cooldown = True
        elif screen == "Dif Select":
            gameDisplay.blit(font_60.render(Map, True, (0, 0, 0)), (400-int(font_60.size(Map)[0]/2), 20))


            #Different Difficulty Buttons
            for i in range(3):
                pygame.draw.rect(gameDisplay, (0, 100, 0), (50+250*i, 400, 200, 150), 0)
                pygame.draw.rect(gameDisplay, (0, 200, 0), (50+250*i, 400, 200, 150), 3)
                gameDisplay.blit(font_30.render(Diff[i], True, (0, 0, 0)), (150+250*i-int(font_30.size(Diff[i])[0]/2), 440))

                if 50+250*i <= pos[0] <= 50+250*i+200 and 400 <= pos[1] <= 550 and pressed[0] == 1 and not cooldown:
                    main.game_loop(False, MapName, Diff[i])

            #The Continue Button
            pygame.draw.rect(gameDisplay, (0, 100, 0), (50, 290, 120, 95), 0)
            pygame.draw.rect(gameDisplay, (0, 200, 0), (50, 290, 120, 95), 3)
            gameDisplay.blit(font_20.render("Continue", True, (0, 0, 0)), (60, 330))


            #Displays wave and difficulty of your continue
            gameDisplay.blit(font_20.render("Wave: " + str(data[SaveNames.index(MapName)*2]), True, (0, 0, 0)), (60, 310))
            if data[SaveNames.index(MapName)*2+1] != "0":
                gameDisplay.blit(font_20.render(str(data[SaveNames.index(MapName)*2+1]), True, (0, 0, 0)), (60, 290))
            else:
                gameDisplay.blit(font_20.render("Medium", True, (0, 0, 0)), (60, 290))

            if 50 <= pos[0] <= 170 and 290 <= pos[1] <= 385 and pressed[0] == 1 and not cooldown:
                main.game_loop(True, MapName)
            
            #The Back Button
            pygame.draw.rect(gameDisplay, (100, 0, 0), (10, 10, 100, 75), 0)
            pygame.draw.rect(gameDisplay, (200, 0, 0), (10, 10, 100, 75), 3)
            gameDisplay.blit(font_30.render("Back", True, (0, 0, 0)), (25, 20))

            if 10 <= pos[0] <= 110 and 10 <= pos[1] <= 85 and pressed[0] == 1 and not cooldown:
                screen = "Map Select"
                cooldown = True

            if pressed[0] == 0:
                cooldown = False

        pygame.display.flip()
        fpsClock.tick(fps)

if __name__ == "__main__":
    MainMenu()
