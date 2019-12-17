import pygame, random, sys, math, os, tower, waves, monsters, mainMenu
from pygame.locals import *
 
pygame.init()
 
fps = 120
fpsClock = pygame.time.Clock()
 
width, height = 840, 580
gameDisplay = pygame.display.set_mode((width, height), pygame.SRCALPHA, 32)

font_20 = pygame.font.Font("IBMPlexSans-Regular.ttf", 20)
font_15 = pygame.font.Font("IBMPlexSans-Regular.ttf", 15)

# TODO List:
#
# Towers:
# Ninja Tower (Detects Camo) (Finished)
# Flamethrower (Pops Lead) (Finished)
# Ice Tower (Slows/Pops Lead) (Finished)
# Explosion Factory (Pops Lead/Aoe Damage) (Finished)
# Money Tower (Generates Money) (Working On)
# Glaive Tower
# Super Tower
#
# Bloons:
# Lead Bloons (Finished)
# Camo Bloons (Finished)
# Stronger Bloons (On going)
#
# Late Game Content:
# Main Menu
# Different Maps

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
    
def setup_Board(board):
    """Function used to setup the board with all path tiles"""
    #Making the pathing
    for i in range(7):
        board[5][i] = 1
    for i in range(3):
        board[2][i+3] = 1
    for i in range(3):
        board[4-i][6] = 1
    for i in range(8):
        board[2+i][3] = 1
    for i in range(10):
        board[9][4+i] = 1
    for i in range(5):
        board[8-i][13] = 1
    for i in range(2):
        board[4][14+i] = 1

    '''Print out all path tiles cord on the board
    for j, row in enumerate(board):
        for i, tile in enumerate(row):
            if tile == 1: print(i, j)'''

    return board



class Selection():
    """Class to buy and select towers"""
    def __init__(self):
        self.selected = 0
        self.cooldown = 0
        self.bought = 0
        self.Costs = [100, 200, 300, 400, 500, 600, 700, 800]
        self.names = ["Dart Tower", "Ninja Tower", "Flamethrower", "Ice Tower",
                      "Explosion Factory", "Money Tower", "Glaive Tower", "Super Tower"]
        
    
    def update(self, board, cash):
        pressed, pos = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #Drawing the selection of towers
        for j in range(4):
            for i in range(2):
                if 660+i*100 <= pos[0] <= 660+i*100+60 and 150+j*70 <= pos[1] <= 150+j*70+60 and pressed[0] == 1:
                    self.selected = i+j*2+1
                    self.cooldown = 20

        #Displays costs of certain towers
        if self.selected != 0:
            gameDisplay.blit(font_20.render(str(self.names[self.selected-1]), True, (0, 0, 0)), (
                740-int(font_20.size(str(self.names[self.selected-1]))[0]/2), 425))
            gameDisplay.blit(font_20.render("Cost: " + str(self.Costs[self.selected-1]), True, (0, 0, 0)), (690, 450))


        #Buying a new tower
        if self.cooldown <= 0 and self.selected != 0 and 0 <= pos[0] <= 640 and 0 <= pos[1] <= 480 and pressed[0] == 1:
            if board[int(pos[1]/40)][int(pos[0]/40)] == 0 and cash >= self.Costs[self.selected-1]:
                board[int(pos[1]/40)][int(pos[0]/40)] = tower.Tower(int(pos[0]/40)*40+5, int(pos[1]/40)*40+5, self.selected)
                board[int(pos[1]/40)][int(pos[0]/40)].selected = True
                cash -= self.Costs[self.selected-1]
                self.bought = 1
                if keys[303] != 1 and keys[304] != 1:
                    self.selected = 0
        else:
            self.cooldown -= 1

        if keys[303] != 1 and keys[304] != 1 and self.bought != 0:
            self.selected = 0
            self.bought = 0

        return board, cash
    





class Start():
    def __init__(self):
        self.x, self.y  = 650, 490
        self.width, self.height = 180, 80
        self.speed = 0
        self.changed = False

    def draw(self):
        pygame.draw.rect(gameDisplay, (140, 110, 70), (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(gameDisplay, (110, 80, 40), (self.x, self.y, self.width, self.height), 3)
        if self.speed >= 1:
            pygame.draw.polygon(gameDisplay, (0, 150, 0), [(710, 500), (710, 560), (750, 530)], 0)
        if self.speed >= 2:
            pygame.draw.polygon(gameDisplay, (0, 150, 0), [(740, 500), (740, 560), (780, 530)], 0)
        if self.speed == 0:
            pygame.draw.polygon(gameDisplay, (0, 150, 0), [(710, 500), (710, 560), (750, 530)], 2)

    def update(self):
        self.draw()

        #Updating the speed
        pressed, pos = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        if ((pressed[0] == 1 and self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height)or(keys[32]==1)) and not self.changed:
            self.changed = True
            self.speed += 1
            if self.speed > 2:
                self.speed = 1

        if not ((pressed[0] == 1 and self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height)or(keys[32]==1)):
            self.changed = False

class AutoPlay():
    def __init__(self):
        self.x, self.y = 200, 150
        self.width, self.height = 70, 70
        self.switch = False
        self.cooldown = 0

    def draw(self):
       
        pygame.draw.rect(gameDisplay, (140, 110, 70), (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(gameDisplay, (110, 80, 40), (self.x, self.y, self.width, self.height), 3)
        if self.switch:
            pygame.draw.line(gameDisplay, (0, 200, 0), (self.x + 10, self.y + 10), (self.x + 45, self.y + 60), 5)
            pygame.draw.line(gameDisplay, (0, 200, 0), (self.x + 45, self.y + 60), (self.x + 60, self.y + 40), 5)
        else:
            pygame.draw.line(gameDisplay, (100, 0, 0), (self.x + 10, self.y + 10), (self.x + 60, self.y + 60), 3)
            pygame.draw.line(gameDisplay, (100, 0, 0), (self.x + 60, self.y + 10), (self.x + 10, self.y + 60), 3)
 

    def update(self):
        self.draw()

        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height and pressed[0] == 1 and self.cooldown == 0:
            self.switch = not self.switch
            self.cooldown = 1

        if pressed[0] != 1:
            self.cooldown = 0

class Settings():
    def __init__(self):
        self.x, self.y = 580, 510
        self.width, self.height = 30, 30
        self.switch = False
        self.cooldown = 0
        self.autoPlay = AutoPlay()

    def draw(self):
       
        pygame.draw.rect(gameDisplay, (140, 110, 70), (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(gameDisplay, (110, 80, 40), (self.x, self.y, self.width, self.height), 3)
    

    def settingsLoad(self):

        run = True
        while run:
            
            #Getting the mouse cordinates
            pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

            #Drawing the background of the settings window
            pygame.draw.rect(gameDisplay, (160, 130, 90), (150, 100, 400, 300), 0)
            pygame.draw.rect(gameDisplay, (110, 80, 40), (150, 100, 400, 300), 3)

            #Drawing the exit button
            pygame.draw.rect(gameDisplay, (150, 0, 0), (515, 85, 50, 50), 0)
            pygame.draw.rect(gameDisplay, (100, 0, 0), (515, 85, 50, 50), 2)
            pygame.draw.line(gameDisplay, (50, 0, 0), (520, 90), (560, 130), 3)
            pygame.draw.line(gameDisplay, (50, 0, 0), (560, 90), (520, 130), 3)
            if 515 <= pos[0] <= 565 and 85 <= pos[1] <= 135 and pressed[0] == 1:
                run = False
            
            #The autoplay button
            gameDisplay.blit(font_20.render("Autoplay", True, (0, 0, 0)), (195, 120))
            self.autoPlay.update()

            #Settings bar at the top
            pygame.draw.rect(gameDisplay, (160, 130, 90), (300, 75, 100, 50), 0)
            pygame.draw.rect(gameDisplay, (110, 80, 40), (300, 75, 100, 50), 3)
            gameDisplay.blit(font_20.render("Settings", True, (0, 0, 0)), (310, 85))

            for event in pygame.event.get():
                if event.type == QUIT:
                  pygame.quit()
                  sys.exit()

            pygame.display.flip()
            fpsClock.tick(fps)


    def update(self):
        self.draw()

        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height and pressed[0] == 1 and self.cooldown == 0:
            self.settingsLoad()
            self.cooldown = 1

        if pressed[0] != 1:
            self.cooldown = 0
     
def game_loop(load):
    """Main Function"""

    width, height = 16, 12
    Board = setup_Board([[0]*width for _ in range(height)])
    Lives, Cash = 100, 750
    selection = Selection()
    score = 0
    startButton = Start()
    Images = load_images("Images")
    abilityCooldown = False
    settings = Settings()
    cooldown = 100

    #Generating each of the waves
    wave = 1

    #Loading your save file
    if load:
        file = open("SaveFile/saveFile.txt", "r")
        data = file.readline().split("#")
        if len(data) >= 197:
            count = 0
            #Loading all the tiles
            for j, row in enumerate(Board):
                    for i, tile in enumerate(row):
                        if data[count] == "2":
                            count += 1
                            #Loading all variables for a tower
                            Board[j][i] = tower.Tower(i*40+5, j*40+5, int(data[count]))
                            Board[j][i].pops = int(data[count+1])
                            Board[j][i].score = int(data[count+2])
                            Board[j][i].pierce = int(data[count+3])
                            Board[j][i].damage = int(data[count+4])
                            Board[j][i].speed = float(data[count+5])
                            Board[j][i].shotAmount = int(data[count+6])
                            Board[j][i].size = int(data[count+7])
                            Board[j][i].path = int(data[count+8])
                            Board[j][i].seeking = data[count+9] == "True"
                            Board[j][i].bulletSpeed = float(data[count+10])
                            Board[j][i].camo = data[count+11] == "True"
                            Board[j][i].dead = data[count+12] == "True"
                            Board[j][i].fireDamage = int(data[count+13])
                            Board[j][i].fireLength = float(data[count+14])
                            Board[j][i].fireLasting = float(data[count+15])
                            Board[j][i].Permaslow = data[count+16] == "True"
                            Board[j][i].slowAmount = float(data[count+17])
                            Board[j][i].ExplodeTime = float(data[count+18])
                            Board[j][i].bombRange = int(data[count+19])
                            Board[j][i].crateValue = int(data[count+20])
                            Board[j][i].autoCollect = data[count+21] == "True"
                            Board[j][i].expireTime = int(data[count+22])
                            Board[j][i].glaiveCount = int(data[count+23])
                            Board[j][i].glaiveSpeed = float(data[count+24])
                            Board[j][i].glaiveRings = int(data[count+25])
                            Board[j][i].selected = False
                            count += 26


                            #Loads all upgrades
                            for h, item in enumerate(Board[j][i].upgrades):
                                for g, subItem in enumerate(item):
                                    Board[j][i].upgrades[h][g] = int(data[count])
                                    count += 1
                  
                            Board[j][i].currentUpgrade = [int(data[count]), int(data[count+1])]
                            count += 2

                            for item in Board[j][i].ability:
                                Board[j][i].ability.append([data[count], int(data[count+1]), int(data[count+2]), int(data[count+3])])
                                count += 4

                        else:
                            Board[j][i] = int(data[count])
                            count += 1

            Cash = int(data[count])
            Lives = int(data[count+1])
            settings.autoPlay.switch = data[count+3] == "True"
            score = int(data[count+2])
            wave = int(data[count+4])
            count += 5
        else:
            print("Invalid Save File")

    #Generating the monsters
    Monsters = waves.genEnemies(wave, Images)
          
    game_run = True
    while game_run:

        #Grabbing mouse cordinates
        pos = pygame.mouse.get_pos()

        gameDisplay.fill((130,90,50))

        #Drawing the background
        for j, row in enumerate(Board):
            for i, tile in enumerate(row):
                if Board[j][i] == 0:
                    Color = (0, 150, 0)
                elif Board[j][i] == 1:
                    Color = (210, 180, 140)
                else:
                    Color = (0, 150, 0)
                pygame.draw.rect(gameDisplay, Color, (i*40,j*40,40,40), 0)
                pygame.draw.rect(gameDisplay, (0, 150, 0), (i*40, j*40, 40, 40), 1)

        #Updating all monsters on the board:
        for monster in Monsters:
            if monster[1] > 0:
                monster[1] -= 1*startButton.speed
            else:
                if monster[0].dead:
                    Monsters.pop(Monsters.index(monster))
                else:
                    Lives = monster[0].update(Lives, startButton.speed, gameDisplay)
                    if monster[0].duplicate:
                        monster[0].duplicate = False
                        tempMonster = [monsters.Monster(5,wave,monster[0].camo, Images),monster[1]-30]
                        tempMonster[0].x, tempMonster[0].y = monster[0].x, monster[0].y
                        tempMonster[0].step = monster[0].step
                        tempMonster[0].cooldown = 5
                        tempMonster[0].hit = monster[0].hit
                        tempMonster[0].fire = monster[0].fire
                        tempMonster[0].speedModifier = monster[0].speedModifier
                        Monsters.append(tempMonster)
                    if len(monster[0].addMonster) != 0:
                        for i, mons in enumerate(monster[0].addMonster):
                            tempMonster = [monsters.Monster(mons,wave,monster[0].camo, Images),monster[1]-30*(i+1)]
                            tempMonster[0].x, tempMonster[0].y = monster[0].x, monster[0].y
                            tempMonster[0].step = monster[0].step
                            tempMonster[0].cooldown = 5
                            tempMonster[0].hit = monster[0].hit
                            tempMonster[0].fire = monster[0].fire
                            tempMonster[0].speedModifier = monster[0].speedModifier
                            Monsters.append(tempMonster)
                    monster[0].addMonster = []
                                
        if len(Monsters) == 0:

            #Starting the new wave
            Cash += 100+wave+1
            wave += 1
            Monsters = waves.genEnemies(wave, Images)
            if not settings.autoPlay.switch:
                startButton.speed = 0
            for j, row in enumerate(Board):
                for i, tile in enumerate(row):
                    try:
                        tile = int(tile)
                    except Exception:
                        tile.Projectiles = []

            #Saving after a wave ends
            data = ""
            for j, row in enumerate(Board):
                for i, tile in enumerate(row):
                    stop = False
                    try:
                        tile = int(tile)
                    except Exception:
                        data += "2" + "#"
                        for item in [tile.rank, tile.pops, tile.score, tile.pierce, tile.damage, tile.speed, tile.shotAmount, tile.size, tile.path, tile.seeking,
                                     tile.bulletSpeed, tile.camo, tile.dead, tile.fireDamage, tile.fireLength, tile.fireLasting, tile.Permaslow, tile.slowAmount,
                                     tile.ExplodeTime, tile.bombRange, tile.crateValue, tile.autoCollect, tile.expireTime, tile.glaiveCount, tile.glaiveSpeed,
                                     tile.glaiveRings]:
                            data += str(item) + "#"
                        for item in tile.upgrades:
                            for subItem in item:
                                data += str(subItem) + "#"
                        for item in tile.currentUpgrade:
                            data += str(item) + "#"
                        for ability in tile.ability:
                            for item in ability:
                                data += str(item) + "#"
                        stop = True
                    if not stop:
                        data += str(tile) + "#"

            data += str(Cash) + "#"
            data += str(Lives) + "#"
            data += str(score) + "#"
            data += str(settings.autoPlay.switch) + "#"
            data += str(wave) + "#"

            file = open("SaveFile/saveFile.txt", "w")
            file.write(data)

        #Making the selection bar
        pygame.draw.rect(gameDisplay, (130, 90, 50), (640, 0, 200, 580), 0)
        ColorBoard = [[(200, 0, 0), (0, 0, 200)], [(200, 200, 0), (0, 200, 200)], [(100, 100, 100), (0, 200, 0)], [(200, 200, 200), (100, 150, 200)]]
        for j in range(4):
            for i in range(2):
                pygame.draw.rect(gameDisplay, (140, 90, 40), (660+i*100, 150+j*70, 60, 60), 0)
                pygame.draw.rect(gameDisplay, (210, 180, 140), (660+i*100, 150+j*70, 60, 60), 3)
                if (j != 1 or i != 0) and (j != 0 or i != 1) and (j != 1 or i != 1):
                    pygame.draw.rect(gameDisplay, ColorBoard[j][i], (660+i*100+10, 150+j*70+10, 40, 40), 0)
                elif j == 0 and i == 1:
                    gameDisplay.blit(pygame.transform.scale(Images["NinjaBase"], (30, 30)), (660+i*100+15, 150+j*70+20))
                    gameDisplay.blit(pygame.transform.scale(Images["NinjaGun"], (30, 40)), (660+i*100+15, 150+j*70+5))
                elif j == 1 and i == 1:
                    gameDisplay.blit(pygame.transform.scale(Images["IceTower"], (30, 30)), (660+i*100+15, 150+j*70+20))                  
                else:
                    gameDisplay.blit(pygame.transform.scale(Images["Flamethrower"], (40, 60)), (660+i*100+10, 150+j*70))

        #Drawing Lives/Cash
        gameDisplay.blit(pygame.transform.scale(Images["Heart"], (20, 20)), (660, 60))
        gameDisplay.blit(pygame.transform.scale(Images["InstantMoney"], (20, 20)), (660, 20))
        gameDisplay.blit(font_20.render(str(Cash), True, (0, 0, 0)), (690, 16))
        gameDisplay.blit(font_20.render(str(Lives), True, (0, 0, 0)), (690, 56))
        gameDisplay.blit(font_20.render("Wave: " + str(wave), True, (0, 0, 0)), (660, 96))

        if Lives <= 0:
            game_run = False

        #Event handler
        for event in pygame.event.get():
            if event.type == QUIT:
              pygame.quit()
              sys.exit()

        #Drawing all towers:
        stop = False
        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        for j, row in enumerate(Board):
            for i, tile in enumerate(row):
                try:
                    tile = int(tile)
                except Exception:
                    tile.update(Monsters, startButton.speed, Cash, Board, Images, gameDisplay)
                    if tile.x <= pos[0] <= tile.x + tile.width and tile.y <= pos[1] <= tile.y + tile.height and pressed[0] == True:
                        for h, k in enumerate(Board):
                            for l, s in enumerate(k):
                                try:
                                    s = int(s)
                                except Exception:
                                    s.selected = False
                        tile.selected = True
                        stop = True
                    Cash += tile.cash

                    #Checking to see whether something was bought today
                    if tile.cash < 0 or not (0 <= pos[0] <= 640 and 0 <= pos[1] <= 480):
                        stop = True
                        

                    tile.cash = 0
                    score += tile.score
                    tile.score = 0

                    if tile.dead == True:
                        Board[j][i] = 0
        if stop == False and pressed[0] == True:
            for j, row in enumerate(Board):
                for i, tile in enumerate(row):
                    try:
                        tile = int(tile)
                    except Exception:
                        tile.selected = False
        

        Board, Cash = selection.update(Board, Cash)

        #The start button
        startButton.update()

        #Updates the settings
        gameDisplay.blit(font_15.render("Settings", True, (0, 0, 0)), (565, 490))
        settings.update()

        #Updating all crates so their drawn on a higher level then towers
        for j, row in enumerate(Board):
            for i, tile in enumerate(row):
                try:
                    tile = int(tile)
                except Exception:
                    if tile.rank == 6:
                        for crate in tile.Crates:
                            crate.update(startButton.speed, gameDisplay)

                            if crate.expireTime <= 0:
                                tile.Crates.pop(tile.Crates.index(crate))

                            if crate.collected:
                                Cash += crate.value
                                tile.Crates.pop(tile.Crates.index(crate))
                    elif tile.rank == 7:
                        for glaive in tile.Glaives:
                            glaive.update(startButton.speed, gameDisplay)

        #Abilities
        Abilities = []
        for j, row in enumerate(Board):
            for i, tile in enumerate(row):
                try:
                    tile = int(tile)
                except Exception:
                    for ability in tile.ability:
                        #Checks for all ready abilities
                        if ability[1] == 0:
                            Abilities.append(ability[0])
                        elif ability[1] == -1:
                            pass
                        else:
                            ability[1] -= 1

        
        if len(Abilities) != 0:
            alreadyUsed = {}
            for ability in Abilities:
                if ability not in alreadyUsed.keys():
                    alreadyUsed[ability] = 1
                else:
                    alreadyUsed[ability] += 1

            count = 0
            for k, v in alreadyUsed.items():
                pygame.draw.rect(gameDisplay, (210, 180, 140), (10+55*count, 430, 40, 40), 0)
                pygame.draw.rect(gameDisplay, (180, 140, 80), (10+55*count, 430, 40, 40), 2)
                if k == "Bullet Time":
                    
                    pygame.draw.rect(gameDisplay, (255,215,0), (20+55*count, 435, 15, 10), 0)
                    pygame.draw.circle(gameDisplay, (255, 215, 0), (35+55*count, 440), 5, 0)                

                    pygame.draw.circle(gameDisplay, (255, 255, 255), (25+55*count, 458), 10, 0)
                    pygame.draw.circle(gameDisplay, (0, 0, 0), (25+55*count, 458), 11, 1)
                    pygame.draw.line(gameDisplay, (0, 0, 0), (25+55*count, 458), (25+55*count, 450), 2)
                    pygame.draw.line(gameDisplay, (0, 0, 0), (25+55*count, 458), (20+55*count, 455), 2)

                elif k == "Forest Fire":
                    gameDisplay.blit(pygame.transform.scale(Images["ForestFire"],(20,30)),(20+55*count,435))

                elif k == "The Arctic":
                    gameDisplay.blit(pygame.transform.scale(Images["TheArctic"],(100,30)),(-20+55*count,435))

                elif k == "Smoke Bomb":
                    gameDisplay.blit(pygame.transform.scale(Images["SmokeBomb"],(50,50)),(55*count,425))

                elif k == "Instant Money":
                    gameDisplay.blit(pygame.transform.scale(Images["InstantMoney"],(30,30)),(15+55*count,435))

                elif k == "Complete Reform":
                    gameDisplay.blit(pygame.transform.scale(Images["CompleteReform"],(30,30)),(15+55*count,435))
                elif k == "Unleash Havoc":
                    gameDisplay.blit(pygame.transform.scale(Images["UnleashHavoc"],(30,30)),(15+55*count,435))
                    
                gameDisplay.blit(font_20.render(str(v), True, (0, 0, 0)), (40+55*count, 450))

                

                stop = False
                if 10+55*count <= pos[0] <= 10+55*count+40 and 430 <= pos[1] <= 470 and pressed[0] == 1:
                    for j, row in enumerate(Board):
                        for i, tile in enumerate(row):
                            try:
                                tile = int(tile)
                            except Exception:
                                for ability in tile.ability:
                                    stop2 = False
                                    for a in tile.effects:
                                        if a[0] == ability[0]:
                                            stop2 = True
                                    if not stop and ability[0] == k and not stop2 and not abilityCooldown:
                                        abilityCooldown = True
                                        stop = True
                                        ability[1] = ability[2] + 0
                                        tile.effects.append([k,ability[3],False])
                count += 1

        if pressed[0] == 0:
            abilityCooldown = False
                    
        #Drawing range of selected tower
        for j, row in enumerate(Board):
            for i, tile in enumerate(row):
                try:
                    tile = int(tile)
                except Exception:
                    if tile.selected:
                        pygame.draw.circle(gameDisplay, (0, 0, 0, 125), (tile.x+int(tile.width/2), tile.y+int(tile.height/2)),int(tile.range), 2)
        
        pygame.display.flip()
        fpsClock.tick(fps)

    print("Score: " + str(score))

if __name__ == "__main__":
    mainMenu.MainMenu()
