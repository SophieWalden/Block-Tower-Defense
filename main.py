import pygame, random, sys, math, os
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
#
# Bloons:
# Lead Bloons (Finished)
# Camo Bloons (Finished)
# Stronger Bloons (On going)
#
# Late Game Content:
# Main Menu
# Different Maps

#Changes:
#Flamethrower speed doubled
#Flamethrower range upgrade cost 250 -> 100
#Flamethrower speed upgrade cost 100 -> 250
#Swapped Flamethrower left 1st and 2nd upgrades
#Fixed fire bugs concerning black monsters popping into two
#Added Ice Tower

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

def shorten(Num):
    """Shortens a number"""
    count = 0
    let = ""

    while Num >= 1000:
        Num /= 1000
        count += 1

    Num = str(Num)
    Num2 = ""

    if count >= 1:
        for i in range(Num.index(".")+2):
            Num2 += Num[i]

        Num = Num2

    if count == 1:
        Num += "K"
    if count == 2:
        Num += "M"
    if count == 3:
        Num += "B"
    if count == 4:
        Num += "T"
    if count == 5:
        Num += "q"
    if count == 6:
        Num += "Q"
    if count == 7:
        Num += "s"
    if count == 8:
        Num += "S"

    return Num

class Tower():
    """Class which encapsulates  all towers visuals/mechanics"""
    def __init__(self, x, y, rank):
        self.x, self.y = x, y
        self.width, self.height = 30, 30
        self.rank = rank
        Colors = [(200, 0, 0), (0, 0, 200), (200, 200, 0), (0, 200, 200), (200, 0, 200), (100, 100, 100), (200, 200, 200), (100, 150, 200)]
        self.color = Colors[self.rank-1]
        self.range = 100
        self.Projectiles = []
        self.cooldown = 50
        self.pops = 0
        self.cash = 0
        self.score = 0
        self.upgrades = [[0, 0, 0, 0], [0, 0, 0, 0]]
        self.currentUpgrade = [0,0]
        self.selected = True
        self.pierce = 1
        self.damage = 1
        self.speed = 1
        self.buyCooldown = 0
        self.shotAmount = 1
        self.size = 10
        self.path = 0
        self.seeking = False
        self.bulletSpeed = 10
        self.ability = []
        self.camo = False
        self.effects = []
        self.dead = False
        self.fireDamage = 1
        self.fireLength = 50
        self.fireLasting = 150
        self.Permaslow = False
        self.slowAmount = 0.75

        self.description = [[["",0]]*4]*2
        #Putting in all the distinct upgrades
        if rank == 1:
            #Dart Monkeys
            self.descriptions =[[["Long Range Shot",100],["Extra Range Shot",200],["Double Damage",600],["Big Shot",2000]],
                                [["Piercing Darts", 150],["Faster Tower", 300],["Triple Shot", 450],["Speed 4 Days", 3500]]]

            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount, self.seeking, self.bulletSpeed, self.camo, self.value, self.fire = 1,1,1,100,10,1, False, 10, False, 100, False
            self.lead = False
        elif rank == 2:
            #Ninja Monkeys
            self.descriptions =[[["Ninja Discipline",150],["Sharp Shruks",275],["Double Trouble",750],["Grandjitsu",2750]],
                                [["Seeking Shruks", 150],["Small, but Deadly", 300],["Slow, but Poweful", 450],["Bullet Time", 4500]]]

            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount, self.seeking, self.bulletSpeed, self.camo, self.value, self.fire  = 1,1,1,100,10,1, False, 10, True, 200, False
            self.lead = False
        elif rank == 3:
            #Flamethrower
            self.descriptions =[[["Ranged Flames",100],["Faster Flames",250],["Damaging Fire",600],["Tracking Fire", 6500]],
                                [["Long Lasting Fire", 175],["Extra Fire", 200],["Fire for all", 800],["Forest Fire", 3000]]]
            
            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount, self.seeking, self.bulletSpeed, self.camo, self.value, self.fire  = 1,0,0.5,50,15,1, False, 10, True, 300, True
            self.lead = True

        elif rank == 4:
            #Ice Tower
            self.descriptions =[[["Fast Freezing",100],["Ranged Ice",250],["Lead Destruction",600],["Frozen in Time", 6500]],
                                [["Slow Monsters", 175],["Damaging Ice", 200],["Slowed For Life", 800],["The Artic", 3000]]]
            
            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount  = 1,0,0.5,65,10,0
            self.seeking, self.bulletSpeed, self.camo, self.value, self.fire = False, 10, False, 400, False
            self.lead = False

    def draw(self):
        pygame.draw.rect(gameDisplay, (0,150,0), (self.x-5, self.y-5, 40, 40), 0)
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.width, self.height),0)
        
    def attack(self, Monsters, speed):

        #Display Range of tower:
        #pygame.draw.circle(gameDisplay, (0, 0, 0), (self.x, self.y), self.range, 0)

        #Upgrades set by effects
        effect = [1]
        for affect in self.effects:
            if affect[0] == "Bullet Time":
                effect[0] *= 3
            elif affect[0] == "Forest Fire" and not affect[2]:
                for i in range(36):
                    self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), i*0.2, self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000)))
                affect[2] = True
            elif affect[0] == "The Arctic":
                for monster in Monsters:
                    monster[0].speedModifier = [0.4, 100]
            
            affect[1] -= 1
            if affect[1] <= 0:
                self.effects.pop(self.effects.index(affect))
                    
        #Checking to see if there is a monster in range
        if self.rank in [1,2, 3]  and self.cooldown <= 0:
            for monster in Monsters:
                if math.sqrt((monster[0].x - self.x)**2 + (monster[0].y - self.y)**2) <= self.range and self.cooldown <= 0:
                    if not monster[0].camo or (monster[0].camo and self.camo):

                        angle = math.atan2((self.y-monster[0].y),(self.x-monster[0].x))
                        
                        #print("Self: ", (self.x, self.y), " Monster: ", (monster[0].x, monster[0].y), " ", math.atan2((monster[0].y-self.y),(monster[0].x-self.x)), angle)
                        if self.shotAmount == 1:
                            self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), angle, self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000)))
                        else:
                            for i in range(self.shotAmount):
                                self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), angle-0.2*(int(self.shotAmount/2)-i), self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000)))
                        self.cooldown = 50
        else:
            self.cooldown -= 1*speed*self.speed*effect[0]

        #Ice Tower
        if self.rank == 4 and self.cooldown <= 0:
            for monster in Monsters:
                if math.sqrt((monster[0].x - self.x)**2 + (monster[0].y - self.y)**2) <= self.range and self.cooldown <= 0:
                    if monster[0].speedModifier[0] >= self.slowAmount:
                        monster[0].speedModifier = [self.slowAmount, 50]
                    if self.Permaslow:
                        monster[0].permaslow = True
                    if self.damage != 0 and ((monster[0].rank == 7 and self.lead) or not monster[0].rank == 7):
                        monster[0].ReRank(monster[0].rank-self.damage)
                        if monster[0].rank >= 6 and monster[0].rank - self.damage < 6:
                            monster[0].duplicate = True
                        self.pops += 1
                        self.score += 1
                        self.cash += self.damage
            self.cooldown = 50


        #Updating all the towers projectiles
        for projectile in self.Projectiles:
            projectile.update(speed)
            stop = False
            for monster in Monsters:
                if pygame.sprite.collide_rect(projectile, monster[0]) == True and not stop and projectile.id not in monster[0].hit and ((self.fire and not monster[0].fire[0]) or not self.fire) and (((monster[0].rank == 7) == self.lead) or not monster[0].rank == 7):
                    self.cash += self.damage
                    if monster[0].rank >= 6 and monster[0].rank - self.damage < 6:
                        monster[0].duplicate = True
                    if self.damage != 0:
                        monster[0].ReRank(monster[0].rank-self.damage)
                    monster[0].hit.append(projectile.id)
                    if self.fire:
                        monster[0].fire = [True, self.fireLength, self.fireLength, self.fireLasting, self.fireDamage]
                    stop = True
                    self.pops += 1
                    self.score += 1
                    if self.seeking == True:
                        for monster in Monsters:
                            if math.sqrt((monster[0].x - projectile.x)**2 + (monster[0].y - projectile.y)**2) <= self.range*2 and projectile.id not in monster[0].hit:
                                angle = math.atan2((projectile.y-monster[0].y),(projectile.x-monster[0].x))
                                projectile.angle = angle
            if stop:
                projectile.pierce -= 1
                if projectile.pierce <= 0:
                    self.Projectiles.pop(self.Projectiles.index(projectile))
            else:
                if not 0 <= projectile.x <= 640 or not 0 <= projectile.y <= 480:
                    self.Projectiles.pop(self.Projectiles.index(projectile))
        return Monsters

    def upgrade(self, cash):
        """All the upgrdes for the towers"""
        if self.selected:

            #Mouse tracking
            pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

            #Drawing the amount of pops
            gameDisplay.blit(font.render("Pops: " + str(shorten(self.pops)), True, (0, 0, 0)), (400, 485))

            #Sell button
            pygame.draw.rect(gameDisplay, (200, 0, 0), (400, 520, 100, 50), 0)
            pygame.draw.rect(gameDisplay, (150, 0, 0), (400, 520, 100, 50), 2)
            gameDisplay.blit(font.render("SELL", True, (0, 0, 0)), (405, 520))
            gameDisplay.blit(font.render(str(shorten(int(self.value*0.75))), True, (0, 0, 0)), (405, 540))
            if 400 <= pos[0] <= 500 and 520 <= pos[1] <= 570 and pressed[0] == 1:
                self.cash += int(self.value*0.75)
                self.dead = True
            
            #Drawing the 2 upgrade boxes
            pygame.draw.rect(gameDisplay, (140, 110, 70), (10, 495, 180, 80), 0)
            pygame.draw.rect(gameDisplay, (110, 80, 40), (10, 495, 180, 80), 3)

            pygame.draw.rect(gameDisplay, (140, 110, 70), (210, 495, 180, 80), 0)
            pygame.draw.rect(gameDisplay, (110, 80, 40), (210, 495, 180, 80), 3)

            for j, row in enumerate(self.upgrades):
                for i, tile in enumerate(row):
 
                    if tile == 0:
                        pygame.draw.rect(gameDisplay, (0, 150, 0), (10+45*i+j*200, 483, 45, 10), 2)
                    else:
                        pygame.draw.rect(gameDisplay, (0, 150, 0), (10+45*i+j*200, 483, 45, 10), 0)

            if pressed[0] == 0:
                self.buyCooldown = 0

            #Showing the upgrades
            for i in range(2):
                if self.currentUpgrade[i] != 4:
                    if self.path == 0 or self.currentUpgrade[i] <= 1 or (self.path == 1 and i == 0) or (self.path == 2 and i == 1):
                    
                        gameDisplay.blit(font.render(str(self.descriptions[i][self.currentUpgrade[i]][0]), True, (0, 0, 0)), (20+200*i, 500))
                        gameDisplay.blit(font.render(str(self.descriptions[i][self.currentUpgrade[i]][1]), True, (0, 0, 0)), (20+200*i, 520))

                if 10+200*i <= pos[0] <= 190+200*i and 495 <= pos[1] <= 575 and pressed[0] == 1:
                    if self.currentUpgrade[i] < 4:
                        if self.descriptions[i][self.currentUpgrade[i]][1] <= cash + self.cash and self.buyCooldown <= 0:
                            if self.path == 0 or (self.currentUpgrade[i] <= 1 or i == self.path-1):
                                self.cash -= self.descriptions[i][self.currentUpgrade[i]][1]
                                self.value += self.descriptions[i][self.currentUpgrade[i]][1]

                                #Adding all the upgrades
                                if self.rank == 1:
                                    #Dart Monkey Upgrades
                                    if i == 0:
                                        if self.currentUpgrade[i] <= 1:
                                            self.range *= 1.25
                                        elif self.currentUpgrade[i] == 2:
                                            self.damage *= 2
                                            self.path = 1
                                        else:
                                            self.size *= 2
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.pierce += 1
                                        elif self.currentUpgrade[i] == 1:
                                            self.speed *= 1.5
                                        elif self.currentUpgrade[i] == 2:
                                            self.shotAmount = 3
                                            self.path = 2
                                        else:
                                            self.speed *= 2


                                elif self.rank == 2:
                                    #Ninja Monkey Upgrades
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.range *= 1.1
                                            self.speed *= 1.25
                                        elif self.currentUpgrade[i] == 1:
                                            self.pierce += 3
                                        elif self.currentUpgrade[i] == 2:
                                            self.shotAmount += 1
                                            self.path = 1
                                        else:
                                            self.shotAmount += 3
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.seeking = True
                                        elif self.currentUpgrade[i] == 1:
                                            self.size = int(self.size/2)
                                            self.damage *= 2
                                        elif self.currentUpgrade[i] == 2:
                                            self.bulletSpeed = int(self.bulletSpeed/2)
                                            self.damage *= 2
                                            self.path = 2
                                        else:
                                            self.ability.append(["Bullet Time",0,1000,200])
                                            
                                elif self.rank == 3:
                                    #Flamethrower Upgrades
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.range *= 2
                                        elif self.currentUpgrade[i] == 1:
                                            self.speed *= 1.25
                                        elif self.currentUpgrade[i] == 2:
                                            self.fireDamage += 1
                                            self.path = 1
                                        else:
                                            self.seeking = True
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.fireLasting = int(self.fireLasting * 1.5)
                                        elif self.currentUpgrade[i] == 1:
                                            self.pierce += 2
                                        elif self.currentUpgrade[i] == 2:
                                            self.pierce += 5
                                            self.path = 2
                                        else:
                                            self.ability.append(["Forest Fire",0,1000,200])

                                elif self.rank == 4:
                                    #Ice Tower Upgrades
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.speed *= 1.5
                                        elif self.currentUpgrade[i] == 1:
                                            self.range *= 1.5
                                        elif self.currentUpgrade[i] == 2:
                                            self.lead = True
                                            self.damage += 1
                                            self.path = 1
                                        else:
                                            self.speed *= 2
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.slowAmount = 0.6
                                        elif self.currentUpgrade[i] == 1:
                                            self.damage += 1
                                        elif self.currentUpgrade[i] == 2:
                                            self.slowAmount = 0.5
                                            self.Permaslow = True
                                            self.path = 2
                                        else:
                                            self.ability.append(["The Arctic",0,750,200])
                                    
                                    
                                
                                self.currentUpgrade[i] += 1
                                self.upgrades[i][self.currentUpgrade[i]-1] = 1
                                self.buyCooldown = 50

            self.buyCooldown -= 1
                
    def update(self, Monsters, speed, cash):
        self.draw()
        Monsters = self.attack(Monsters, speed)
        self.upgrade(cash)

        return Monsters

class Projectile():
    """It's a projectile, towers throw it"""
    def __init__(self, x, y, angle, pierce, size, speed, Id):
        self.x, self.y, self.angle = x, y, angle
        self.OldX, self.OldY = x, y
        self.width, self.height = size, size
        self.speed = speed
        self.pierce = pierce
        self.id = Id

        #Setting up the hitbox
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

    def draw(self):
        pygame.draw.rect(gameDisplay, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        #pygame.draw.line(gameDisplay, (0, 0, 0), (self.x, self.y), (self.OldX, self.OldY), 5)

    def movement(self, speed):
        self.x -= self.speed*math.cos(self.angle)*speed
        self.y -= self.speed*math.sin(self.angle)*speed
       

    def update(self, speed):
        self.draw()
        self.movement(speed)

        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

class Monster():
    """Class for all the enemies"""
    def __init__(self, rank, wave, camo):

        #Setting up base variables
        self.rank = rank
        self.x, self.y = -100, 200
        self.step = 0
        speed = [2, 3, 4, 5, 6, 4, 3]
        modifier = 0.01*(int(wave/50)+1)
        self.speed = speed[self.rank-1] * (1 + (modifier**wave))
        self.height, self.width = 30, 30
        self.dead = False
        Colors = [(200, 0, 0), (0, 0, 200), (0, 200, 0), (255, 255, 0), (255,105,180), (0, 0, 0), (50, 50, 50)]
        self.color = Colors[self.rank-1]
        self.camo = camo
        self.hit = []
        self.fire = [False,0,0,0,0]
        self.speedModifier = [1,0]
        self.permaslow = False
        #All checkpoints on the map
        self.checkpoints = [(6, 5), (6, 2), (3, 2), (3, 9), (13, 9), (13, 4), (17, 4)]
        self.duplicate = False
        self.cooldown = 0

        #Setting up the hitbox
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

    def ReRank(self, new_Rank):
        """Changes the rank of the monster to any other rank"""

        if new_Rank <= 0:
            self.dead = True
        else:
            self.rank = new_Rank
            Colors = [(200, 0, 0), (0, 0, 200), (0, 200, 0), (255, 255, 0), (255,105,180), (0, 0, 0), (50, 50, 50)]
            self.color = Colors[self.rank-1]
            speed = [2, 3, 4, 5, 6, 4, 3]
            self.speed = speed[self.rank-1]
        
        
    def draw(self):
        pygame.draw.rect(gameDisplay, self.color, (self.x + int(self.width/5), self.y + int(self.height/5), self.width, self.height), 0)

        #Drawing camo bloons
        if self.camo:
            if self.rank != 6:
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.8),int(self.color[1]*0.8),int(self.color[2]*0.8)), (self.x + int(self.width/5), self.y + int(self.height/5), int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.5),int(self.color[1]*0.5),int(self.color[2]*0.5)), (self.x + int(self.width/3) + int(self.width/5), self.y + int(self.height/3) + int(self.height/5), int(self.width/3), int(self.height/3)), 0)    
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.75),int(self.color[1]*0.75),int(self.color[2]*0.5)), (self.x + int(self.width/5), self.y + int(self.height/3) + int(self.height/5), int(self.width/3), int(self.height/3)), 0) 
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.5),int(self.color[1]*0.5),int(self.color[2]*0.5)), (self.x + int(self.width/3) + int(self.width/5), self.y + int(self.height/5), int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.3),int(self.color[1]*0.3),int(self.color[2]*0.3)), (self.x + int(self.width/3)*2 + int(self.width/5), self.y + int(self.height/5), int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.5),int(self.color[1]*0.5),int(self.color[2]*0.5)), (self.x + int(self.width/3)*2 + int(self.width/5), self.y + int(self.height/5)+int(self.width/3)*2, int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]*0.75),int(self.color[1]*0.8),int(self.color[2]*0.75)), (self.x + int(self.width/5), self.y + int(self.height/5)+int(self.width/3)*2, int(self.width/3), int(self.height/3)), 0) 
            else:
                pygame.draw.rect(gameDisplay, (int(self.color[0]+50),int(self.color[1]+50),int(self.color[2]+50)), (self.x + int(self.width/5), self.y + int(self.height/5), int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]+30),int(self.color[1]+30),int(self.color[2]+30)), (self.x + int(self.width/3) + int(self.width/5), self.y + int(self.height/3) + int(self.height/5), int(self.width/3), int(self.height/3)), 0)    
                pygame.draw.rect(gameDisplay, (int(self.color[0]+50),int(self.color[1]+50),int(self.color[2]+50)), (self.x + int(self.width/5), self.y + int(self.height/3) + int(self.height/5), int(self.width/3), int(self.height/3)), 0) 
                pygame.draw.rect(gameDisplay, (int(self.color[0]+50),int(self.color[1]+50),int(self.color[2]+50)), (self.x + int(self.width/3) + int(self.width/5), self.y + int(self.height/5), int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]+70),int(self.color[1]+70),int(self.color[2]+70)), (self.x + int(self.width/3)*2 + int(self.width/5), self.y + int(self.height/5), int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]+50),int(self.color[1]+50),int(self.color[2]+50)), (self.x + int(self.width/3)*2 + int(self.width/5), self.y + int(self.height/5)+int(self.width/3)*2, int(self.width/3), int(self.height/3)), 0)
                pygame.draw.rect(gameDisplay, (int(self.color[0]+50),int(self.color[1]+50),int(self.color[2]+50)), (self.x + int(self.width/5), self.y + int(self.height/5)+int(self.width/3)*2, int(self.width/3), int(self.height/3)), 0) 



        if self.fire[0]:
            colors = [(255,0,0), (255,165,0), (255,255,0)]
            for i in range(9):
                pygame.draw.rect(gameDisplay, colors[random.randint(0,2)], (self.x+random.randint(5, 20), self.y+random.randint(5, 20), random.randint(5, 20), random.randint(5, 20)), 0)

        pygame.draw.rect(gameDisplay, (100, 100, 100), (self.x + int(self.width/5), self.y + int(self.height/5), self.width, self.height), 2)

    def movement(self, Lives, speed):

        #Checking to see whether the monster is in range of the next checkpoint
        if (self.checkpoints[self.step][0]*40-self.speed <= self.x <= self.checkpoints[self.step][0]*40+self.speed and
            self.checkpoints[self.step][1]*40-self.speed <= self.y <= self.checkpoints[self.step][1]*40+self.speed):
            self.x, self.y = self.checkpoints[self.step][0]*40, self.checkpoints[self.step][1]*40
            self.step += 1
            if self.step == 7:
                self.dead = True
                Lives -= self.rank
        else:
            #Else move it towards it's next checkpoint
            if self.x < self.checkpoints[self.step][0]*40:
                self.x += int(self.speed*speed*self.speedModifier[0])
            elif self.x > self.checkpoints[self.step][0]*40:
                self.x -= int(self.speed*speed*self.speedModifier[0])
            elif self.y > self.checkpoints[self.step][1]*40:
                self.y -= int(self.speed*speed*self.speedModifier[0])
            elif self.y < self.checkpoints[self.step][1]*40:
                self.y += int(self.speed*speed*self.speedModifier[0])

        if self.fire[0] == True:
            self.fire[1] -= 1
            self.fire[3] -= 1
            if self.fire[1] <= 0:
                self.fire[1] = self.fire[2] + 0
                if self.rank >= 6 and self.rank - self.fire[4] < 6:
                    self.duplicate = True
                self.ReRank(self.rank - self.fire[4])
                

            if self.fire[3] <= 0:
                self.fire[0] = False

        if self.speedModifier[1] <= 0:  
            if not self.permaslow:
                self.speedModifier[0] = 1
            else:
                self.speedModifier[0] = 0.75
        else:
            self.speedModifier[1] -= 1

        return Lives

    def update(self, Lives, speed):
        self.draw()
        if speed != 0:
            if self.cooldown <= 0:
                Lives = self.movement(Lives, speed)
            else:
                self.cooldown -= 1

        #Updating hitbox
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

        
        return Lives
    
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
        
    
    def update(self, board, cash):
        pressed, pos = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        #Drawing the selection of towers
        for j in range(2):
            for i in range(2):
                if 660+i*100 <= pos[0] <= 660+i*100+60 and 150+j*70 <= pos[1] <= 150+j*70+60 and pressed[0] == 1:
                    self.selected = i+j*2+1
                    self.cooldown = 20

        #Displays costs of certain towers
        if self.selected != 0:
            gameDisplay.blit(font.render("Cost: " + str(self.Costs[self.selected-1]), True, (0, 0, 0)), (690, 450))


        #Buying a new tower
        if self.cooldown <= 0 and self.selected != 0 and 0 <= pos[0] <= 640 and 0 <= pos[1] <= 480 and pressed[0] == 1:
            if board[int(pos[1]/40)][int(pos[0]/40)] == 0 and cash >= self.Costs[self.selected-1]:
                board[int(pos[1]/40)][int(pos[0]/40)] = Tower(int(pos[0]/40)*40+5, int(pos[1]/40)*40+5, self.selected)
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
    

def genEnemies(wave):
    """Outputs a list of all enemies based on a certain wave"""
    Monsters = []
    if wave == 1:
        for i in range(20):
            Monsters.append([Monster(1, wave, False),30*i])
    elif wave == 2:
        for i in range(35):
            Monsters.append([Monster(1, wave, False),15*i])
    elif wave == 3:
        for i in range(5):
            Monsters.append([Monster(2, wave, False),60*i])
        for i in range(20):
            Monsters.append([Monster(1, wave, False),30*(i+21)])
    elif wave == 4:
        for j in range(5):
            for i in range(2):
                Monsters.append([Monster(2, wave, False),45*(i+j*10)])
            for i in range(8):
                Monsters.append([Monster(1, wave, False),30*(i+j*10+2)])
    elif wave == 5:
        for j in range(3):
            Monsters.append([Monster(1, wave, False),30*(1+j*10)])
            for i in range(9):
                Monsters.append([Monster(2, wave, False),30*(i+1+j*10)])
    elif wave == 6:
        for j in range(3):
            for i in range(5):
                Monsters.append([Monster(1, wave, False),30*(i*2+j*11)])
                Monsters.append([Monster(2, wave, False),30*(i*2+1+j*11)])
            Monsters.append([Monster(3, wave, False),30*(10+j*11)])
        Monsters.append([Monster(3, wave, False),60*(18)])
    elif wave == 7:
        for j in range(5):
            for i in range(4):
                Monsters.append([Monster(1, wave, False),30*(i*2+j*9)])
                Monsters.append([Monster(2, wave, False),30*(i*2+1+j*9)])
            Monsters.append([Monster(3, wave, False),30*(8+j*9)])
    elif wave == 8:
        for i in range(10):
            Monsters.append([Monster(1, wave, False),30*i])
        for i in range(20):
            Monsters.append([Monster(2, wave, False),30*(i+10)])
        for i in range(14):
            Monsters.append([Monster(3, wave, False),30*(i+30)])
    elif wave == 9:
        for i in range(30):
            Monsters.append([Monster(3, wave, False),45*i])
    elif wave == 10:
        for i in range(102):
            Monsters.append([Monster(2, wave, False),20*i])
    elif wave == 11:
        for j in range(3):
            for i in range(2):
                Monsters.append([Monster(1, wave, False),30*(i+j*11)])
            for i in range(4):
                Monsters.append([Monster(2, wave, False),30*(i*2+j*11)])
                Monsters.append([Monster(3, wave, False),30*(i*2+1+j*11)])
            Monsters.append([Monster(4, wave, False),30*(10+j*11)])
    elif wave == 12:
        for j in range(5):
            for i in range(3):
                Monsters.append([Monster(2, wave, False),30*(i+j*7)])
            for i in range(2):
                Monsters.append([Monster(3, wave, False),30*(i+3+j*7)])
            Monsters.append([Monster(4, wave, False),30*(6+j*7)])
    elif wave == 13:
        for i in range(50):
            Monsters.append([Monster(2, wave, False),15*(i)])
        for i in range(23):
            Monsters.append([Monster(3, wave, False),15*(i+50)])
    elif wave == 14:
        for i in range(10):
            Monsters.append([Monster(3, wave, False),30*(i)])
        for i in range(20):
            Monsters.append([Monster(2, wave, False),30*(i+10)])
        for i in range(8):
            Monsters.append([Monster(4, wave, False),30*(i+30)])
    elif wave == 15:
        for j in range(5):
            Monsters.append([Monster(1, wave, False),30*(1+j*5)])
            Monsters.append([Monster(2, wave, False),30*(2+j*5)])
            Monsters.append([Monster(3, wave, False),30*(3+j*5)])
            Monsters.append([Monster(4, wave, False),30*(4+j*5)])
            Monsters.append([Monster(5, wave, False),30*(5+j*5)])
    elif wave == 16:
        for j in range(8):
            for i in range(5):
                Monsters.append([Monster(3, wave, False),30*(i+j*6)])
            Monsters.append([Monster(4, wave, False),30*(5+j*6)])
    elif wave == 17:
        for i in range(12):
            Monsters.append([Monster(4, wave, False),30*(i)])
    elif wave == 18:
        for i in range(80):
            Monsters.append([Monster(3, wave, False),20*(i)])
    elif wave == 19:
        for i in range(5):
            Monsters.append([Monster(3, wave, False),30*(i)])
        for i in range(7):
            Monsters.append([Monster(5, wave, False),30*(i+5)])
        for i in range(10):
            Monsters.append([Monster(4, wave, False),30*(i+12)])
    elif wave == 20:
        for i in range(5):
            Monsters.append([Monster(6, wave, False),30*(i)])

        Monsters.append(Monster(7, wave, False), 150) 
    elif wave == 21:
        for j in range(7):
            for i in range(5):
                Monsters.append([Monster(4, wave, False),30*(i+j*6)])
            Monsters.append([Monster(5, wave, False),30*(5+j*6)])
    elif wave == 22:
        for i in range(16):
            Monsters.append([Monster(6, wave, False),60*(i)])
    elif wave == 23:
        for i in range(7):
            Monsters.append([Monster(5, wave, False),30*(i*2)])
            Monsters.append([Monster(6, wave, False),30*(i*2+1)])
    elif wave == 24:
        for i in range(5):
            Monsters.append([Monster(3, wave, True),30*(i)])
    else:
        for i in range(random.randint(5,15)):
            n = random.randint(1, 100)
            if n <= 50-wave:
                Monsters.append([Monster(1, wave, random.randint(1,10)==1),random.randint(15,30)*(i)])
            elif n <= 70-wave:
                Monsters.append([Monster(2, wave, random.randint(1,10)==1),random.randint(15,30)*(i)])
            elif n <= 90-wave:
                Monsters.append([Monster(3, wave, random.randint(1,10)==1),random.randint(15,30)*(i)])
            elif n <= 110-wave:
                Monsters.append([Monster(4, wave, random.randint(1,10)==1),random.randint(15,30)*(i)])
            elif n <= 130-wave:
                Monsters.append([Monster(5, wave, random.randint(1,10)==1),random.randint(15,30)*(i)])
            elif n <= 150-wave:
                Monsters.append([Monster(6, wave, random.randint(1,10)==1),random.randint(15,30)*(i)])
            else:
                Monsters.append([Monster(7, wave, False),random.randint(15,30)*(i)])

    
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
    Monsters = genEnemies(wave)
    
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
                    Lives = monster[0].update(Lives, startButton.speed)
                    if monster[0].duplicate:
                        monster[0].duplicate = False
                        tempMonster = [Monster(5,wave,monster[0].camo),monster[1]-30]
                        tempMonster[0].x, tempMonster[0].y = monster[0].x, monster[0].y
                        tempMonster[0].step = monster[0].step
                        tempMonster[0].cooldown = 5
                        tempMonster[0].hit = monster[0].hit
                        tempMonster[0].fire = monster[0].fire
                        tempMonster[0].speedModifier = monster[0].speedModifier
                        Monsters.append(tempMonster)
        if len(Monsters) == 0:
            Cash += 100+wave+1
            wave += 1
            Monsters = genEnemies(wave)
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
        ColorBoard = [[(200, 0, 0), (0, 0, 200)], [(200, 200, 0), (0, 200, 200)], [(200, 0, 200), (100, 100, 100)], [(200, 200, 200), (100, 150, 200)]]
        for j in range(2):
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
                    tile.update(Monsters, startButton.speed, Cash)
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

        #Abilities
        Abilities = []
        for j, row in enumerate(Board):
            for i, tile in enumerate(row):
                try:
                    tile = int(tile)
                except Exception:
                    for ability in tile.ability:
                        #Checks for all ready abilities
                        if ability[1] <= 0:
                            Abilities.append(ability[0])
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
