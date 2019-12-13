import pygame, random, sys, math, os, monster, tower
from pygame.locals import *
 
pygame.init()
 
fps = 120
fpsClock = pygame.time.Clock()
 
width, height = 840, 580
gameDisplay = pygame.display.set_mode((width, height), pygame.SRCALPHA, 32)

font = pygame.font.Font("IBMPlexSans-Regular.ttf", 20)

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
            gameDisplay.blit(font.render(str(self.names[self.selected-1]), True, (0, 0, 0)), (
                740-int(font.size(str(self.names[self.selected-1]))[0]/2), 425))
            gameDisplay.blit(font.render("Cost: " + str(self.Costs[self.selected-1]), True, (0, 0, 0)), (690, 450))


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
    

def genEnemies(wave, Images):
    """Outputs a list of all enemies based on a certain wave"""
    Monsters = []
    if wave == 1:
        for i in range(20):
            Monsters.append([monster.Monster(1, wave, False, Images),30*i])
    elif wave == 2:
        for i in range(35):
            Monsters.append([monster.Monster(1, wave, False, Images),15*i])
    elif wave == 3:
        for i in range(5):
            Monsters.append([monster.Monster(2, wave, False, Images),60*i])
        for i in range(20):
            Monsters.append([monster.Monster(1, wave, False, Images),30*(i+21)])
    elif wave == 4:
        for j in range(5):
            for i in range(2):
                Monsters.append([monster.Monster(2, wave, False, Images),45*(i+j*10)])
            for i in range(8):
                Monsters.append([monster.Monster(1, wave, False, Images),30*(i+j*10+2)])
    elif wave == 5:
        for j in range(3):
            Monsters.append([monster.Monster(1, wave, False, Images),30*(1+j*10)])
            for i in range(9):
                Monsters.append([monster.Monster(2, wave, False, Images),30*(i+1+j*10)])
    elif wave == 6:
        for j in range(3):
            for i in range(5):
                Monsters.append([monster.Monster(1, wave, False, Images),30*(i*2+j*11)])
                Monsters.append([monster.Monster(2, wave, False, Images),30*(i*2+1+j*11)])
            Monsters.append([monster.Monster(3, wave, False, Images),30*(10+j*11)])
        Monsters.append([monster.Monster(3, wave, False, Images),60*(18)])
    elif wave == 7:
        for j in range(5):
            for i in range(4):
                Monsters.append([monster.Monster(1, wave, False, Images),30*(i*2+j*9)])
                Monsters.append([monster.Monster(2, wave, False, Images),30*(i*2+1+j*9)])
            Monsters.append([monster.Monster(3, wave, False, Images),30*(8+j*9)])
    elif wave == 8:
        for i in range(10):
            Monsters.append([monster.Monster(1, wave, False, Images),30*i])
        for i in range(20):
            Monsters.append([monster.Monster(2, wave, False, Images),30*(i+10)])
        for i in range(14):
            Monsters.append([monster.monster.Monster(3, wave, False, Images),30*(i+30)])
    elif wave == 9:
        for i in range(30):
            Monsters.append([monster.Monster(3, wave, False, Images),45*i])
    elif wave == 10:
        for i in range(102):
            Monsters.append([monster.Monster(2, wave, False, Images),20*i])
    elif wave == 11:
        for j in range(3):
            for i in range(2):
                Monsters.append([monster.Monster(1, wave, False, Images),30*(i+j*11)])
            for i in range(4):
                Monsters.append([monster.Monster(2, wave, False, Images),30*(i*2+j*11)])
                Monsters.append([monster.Monster(3, wave, False, Images),30*(i*2+1+j*11)])
            Monsters.append([monster.Monster(4, wave, False, Images),30*(10+j*11)])
    elif wave == 12:
        for j in range(5):
            for i in range(3):
                Monsters.append([monster.Monster(2, wave, False, Images),30*(i+j*7)])
            for i in range(2):
                Monsters.append([monster.Monster(3, wave, False, Images),30*(i+3+j*7)])
            Monsters.append([monster.Monster(4, wave, False, Images),30*(6+j*7)])
    elif wave == 13:
        for i in range(50):
            Monsters.append([monster.Monster(2, wave, False, Images),15*(i)])
        for i in range(23):
            Monsters.append([monster.Monster(3, wave, False, Images),15*(i+50)])
    elif wave == 14:
        for i in range(10):
            Monsters.append([monster.Monster(3, wave, False, Images),30*(i)])
        for i in range(20):
            Monsters.append([monster.Monster(2, wave, False, Images),30*(i+10)])
        for i in range(8):
            Monsters.append([monster.Monster(4, wave, False, Images),30*(i+30)])
    elif wave == 15:
        for j in range(5):
            Monsters.append([monster.Monster(1, wave, False, Images),30*(1+j*5)])
            Monsters.append([monster.Monster(2, wave, False, Images),30*(2+j*5)])
            Monsters.append([monster.Monster(3, wave, False, Images),30*(3+j*5)])
            Monsters.append([monster.Monster(4, wave, False, Images),30*(4+j*5)])
            Monsters.append([monster.Monster(5, wave, False, Images),30*(5+j*5)])
    elif wave == 16:
        for j in range(8):
            for i in range(5):
                Monsters.append([monster.Monster(3, wave, False, Images),30*(i+j*6)])
            Monsters.append([monster.Monster(4, wave, False, Images),30*(5+j*6)])
    elif wave == 17:
        for i in range(12):
            Monsters.append([monster.Monster(4, wave, False, Images),30*(i)])
    elif wave == 18:
        for i in range(80):
            Monsters.append([monster.Monster(3, wave, False, Images),20*(i)])
    elif wave == 19:
        for i in range(5):
            Monsters.append([monster.Monster(3, wave, False, Images),30*(i)])
        for i in range(7):
            Monsters.append([monster.Monster(5, wave, False, Images),30*(i+5)])
        for i in range(10):
            Monsters.append([monster.Monster(4, wave, False, Images),30*(i+12)])
    elif wave == 20:
        for i in range(5):
            Monsters.append([monster.Monster(6, wave, False, Images),30*(i)])

        Monsters.append([monster.Monster(7, wave, False, Images), 150])
    elif wave == 21:
        for j in range(7):
            for i in range(5):
                Monsters.append([monster.Monster(4, wave, False, Images),30*(i+j*6)])
            Monsters.append([monster.Monster(5, wave, False, Images),30*(5+j*6)])
    elif wave == 22:
        for i in range(16):
            Monsters.append([monster.Monster(6, wave, False, Images),60*(i)])
    elif wave == 23:
        for i in range(7):
            Monsters.append([monster.Monster(5, wave, False, Images),30*(i*2)])
            Monsters.append([monster.Monster(6, wave, False, Images),30*(i*2+1)])
    elif wave == 24:
        for i in range(5):
            Monsters.append([monster.Monster(3, wave, True, Images),30*(i)])
    elif wave % 25 == 0 and wave != 25:
        Monsters.append([monster.Monster(10, wave, False, Images),30])
    else:
        for i in range(random.randint(5,15)):
            n = random.randint(1, 100)
            if n <= 50-wave:
                Monsters.append([monster.Monster(1, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 70-wave:
                Monsters.append([monster.Monster(2, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 90-wave:
                Monsters.append([monster.Monster(3, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 110-wave:
                Monsters.append([monster.Monster(4, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 130-wave:
                Monsters.append([monster.Monster(5, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 150-wave:
                Monsters.append([monster.Monster(6, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 175-wave:
                Monsters.append([monster.Monster(7, wave, random.randint(1,100)==1, Images),random.randint(15,30)*(i)])
            elif n <= 200-wave:
                Monsters.append([monster.Monster(8, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 225-wave: 
                Monsters.append([monster.Monster(9, wave, random.randint(1,10)==1, Images),random.randint(15,30)*(i)])
            elif n <= 300-wave:
                Monsters.append([monster.Monster(10, wave, False, Images),random.randint(15,30)*i])
    
    return Monsters



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
        self.x, self.y = 600, 490
        self.width, self.height = 30, 30
        self.switch = False
        self.cooldown = 0

    def draw(self):
        if self.switch:
            color = (110, 80, 40)
        else:
            color = (140, 110, 70)
        pygame.draw.rect(gameDisplay, color, (self.x, self.y, self.width, self.height), 0)
        pygame.draw.rect(gameDisplay, (110, 80, 40), (self.x, self.y, self.width, self.height), 3)

    def update(self):
        self.draw()

        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height and pressed[0] == 1 and self.cooldown == 0:
            self.switch = not self.switch
            self.cooldown = 1

        if pressed[0] != 1:
            self.cooldown = 0
     
def game_loop():
    """Main Function"""

    width, height = 16, 12
    Board = setup_Board([[0]*width for _ in range(height)])
    Lives, Cash = 100, 750
    selection = Selection()
    score = 0
    startButton = Start()
    autoPlay = AutoPlay()
    Images = load_images("Images")
    abilityCooldown = False

    #Generating each of the waves
    wave = 1
    Monsters = genEnemies(wave, Images)
    
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
                        tempMonster = [monster.Monster(5,wave,monster[0].camo, Images),monster[1]-30]
                        tempMonster[0].x, tempMonster[0].y = monster[0].x, monster[0].y
                        tempMonster[0].step = monster[0].step
                        tempMonster[0].cooldown = 5
                        tempMonster[0].hit = monster[0].hit
                        tempMonster[0].fire = monster[0].fire
                        tempMonster[0].speedModifier = monster[0].speedModifier
                        Monsters.append(tempMonster)
                    if len(monster[0].addMonster) != 0:
                        for i, mons in enumerate(monster[0].addMonster):
                            tempMonster = [monster.Monster(mons,wave,monster[0].camo, Images),monster[1]-30*(i+1)]
                            tempMonster[0].x, tempMonster[0].y = monster[0].x, monster[0].y
                            tempMonster[0].step = monster[0].step
                            tempMonster[0].cooldown = 5
                            tempMonster[0].hit = monster[0].hit
                            tempMonster[0].fire = monster[0].fire
                            tempMonster[0].speedModifier = monster[0].speedModifier
                            Monsters.append(tempMonster)
                    monster[0].addMonster = []
                                
        if len(Monsters) == 0:
            Cash += 100+wave+1
            wave += 1
            Monsters = genEnemies(wave, Images)
            if not autoPlay.switch:
                startButton.speed = 0
            for j, row in enumerate(Board):
                for i, tile in enumerate(row):
                    try:
                        tile = int(tile)
                    except Exception:
                        tile.Projectiles = []

        #Making the selection bar
        pygame.draw.rect(gameDisplay, (130, 90, 50), (640, 0, 200, 580), 0)
        ColorBoard = [[(200, 0, 0), (0, 0, 200)], [(200, 200, 0), (0, 200, 200)], [(100, 100, 100), (0, 200, 0)], [(200, 200, 200), (100, 150, 200)]]
        for j in range(4):
            for i in range(2):
                pygame.draw.rect(gameDisplay, (140, 90, 40), (660+i*100, 150+j*70, 60, 60), 0)
                pygame.draw.rect(gameDisplay, (210, 180, 140), (660+i*100, 150+j*70, 60, 60), 3)
                pygame.draw.rect(gameDisplay, ColorBoard[j][i], (660+i*100+10, 150+j*70+10, 40, 40), 0)

        #Drawing Lives/Cash
        pygame.draw.rect(gameDisplay, (0, 200, 0), (660, 20, 20, 20), 0)
        pygame.draw.rect(gameDisplay, (200, 0, 0), (660, 60, 20, 20), 0)
        gameDisplay.blit(font.render(str(Cash), True, (0, 0, 0)), (690, 16))
        gameDisplay.blit(font.render(str(Lives), True, (0, 0, 0)), (690, 56))
        gameDisplay.blit(font.render("Wave: " + str(wave), True, (0, 0, 0)), (660, 96))

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

        #The autoplay button
        autoPlay.update()

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
                    
                gameDisplay.blit(font.render(str(v), True, (0, 0, 0)), (40+55*count, 450))

                

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


game_loop()
