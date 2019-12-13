import pygame, random, sys, math, os
from pygame.locals import *
 
pygame.init()

font = pygame.font.Font("IBMPlexSans-Regular.ttf", 20)


#Classes/Functions this file contains
#Shorten: Shortens a number for easy use
#Glaive/Bomb/Crate/Projectile: All things towers can throw out
#Tower: The main tower class



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

class Glaive():
    """Made for the Glaive Tower"""

    def __init__(self, pos, angle, ring, rotateSpeed, img):
        self.startPos = pos
        self.x, self.y = pos[0], pos[1]
        self.width, self.height = 15, 15
        self.angle = angle
        self.rotateSpeed = rotateSpeed
        if ring == 1:
            self.speed = 50
        else:
            self.speed = 85
        self.ring = ring

        self.id = random.randint(0, 1000000)
        self.cooldown = 10
        self.img = img
        self.ang = 0

        #Setting up the hitbox
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width
        


    def draw(self, gameDisplay):
        #pygame.draw.rect(gameDisplay, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(self.img, (self.width+5, self.height+5)), self.ang), (self.x, self.y))


    def movement(self, speed):
        self.angle += 0.05*speed
        self.x, self.y = self.speed*math.cos(self.angle) + self.startPos[0], self.speed*math.sin(self.angle) + self.startPos[1]

        if (self.x, self.y) == (self.speed*math.cos(0) + self.startPos[0], self.speed*math.sin(0) + self.startPos[0]):
            self.angle = 0
        if self.cooldown <= 0:
            self.id = random.randint(0, 1000000)
            self.cooldown = 10
        else:
            self.cooldown -= 1

        self.ang += 5 * speed
        self.ang %= 360

    def update(self, speed, gameDisplay):
        self.movement(speed)
        self.draw(gameDisplay)

        #Updating Hitbox
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width
        

class Crate():
    """A Crate, full of money, usually dropped by the Money Tower"""

    def __init__(self, startPos, endPos, expireTime, crateValue):
        self.x, self.y = startPos[0], startPos[1]
        self.endPos = endPos
        self.angle = math.atan2((self.y-self.endPos[1]),(self.x-self.endPos[0]))
        self.speed = 3
        self.width, self.height = 20, 20
        self.expireTime = expireTime
        self.collected = False
        self.value = crateValue

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (150, 150, 0), (self.x, self.y, self.width, self.height), 0)

    def movement(self, speed):
        if self.endPos != (self.x, self.y):
            self.x -= self.speed*math.cos(self.angle)*speed
            self.y -= self.speed*math.sin(self.angle)*speed
            if abs(self.endPos[1]-self.y)+abs(self.endPos[0]-self.x) <= self.speed*speed:
                self.x, self.y = self.endPos[0], self.endPos[1]

    def collection(self):
        pos, pressed = pygame.mouse.get_pos(), pygame.mouse.get_pressed()

        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            self.collected = True
        

    def update(self, speed, gameDisplay):
        self.draw(gameDisplay)
        self.movement(speed)
        self.collection()

        self.expireTime -= 1

class Bomb():
    """Used in the explosion factory, throws it at the path, it explodes"""

    def __init__(self, startPos, endPos, speed, explodeTime):
        self.x, self.y = startPos[0], startPos[1]
        self.endPos = endPos
        self.angle = math.atan2((self.y-self.endPos[1]),(self.x-self.endPos[0]))
        self.speed = speed
        self.width, self.height = 20, 20
        self.Explode = explodeTime
        self.Explosion = False
        self.maxExplode = self.Explode + 0

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (50+int(200-(self.Explode/self.maxExplode*100)*2), 50, 50), (self.x, self.y, self.width, self.height), 0)

    def movement(self, speed):
        if self.endPos != (self.x, self.y):
            self.x -= self.speed*math.cos(self.angle)*speed
            self.y -= self.speed*math.sin(self.angle)*speed
            if abs(self.endPos[1]-self.y)+abs(self.endPos[0]-self.x) <= self.speed*speed:
                self.x, self.y = self.endPos[0], self.endPos[1]

    def explode(self, speed):
        if self.Explode > 0:
            self.Explode -= 1*speed
        else:
            self.Explosion = True

    def update(self, speed, gameDisplay):
        self.draw(gameDisplay)
        self.movement(speed)
        self.explode(speed)

    

class Projectile():
    """It's a projectile, towers throw it"""
    def __init__(self, x, y, angle, pierce, size, speed, Id, rank, img=0):
        self.x, self.y, self.angle = x, y, angle
        self.OldX, self.OldY = x, y
        self.width, self.height = size, size
        self.speed = speed
        self.pierce = pierce
        self.id = Id
        self.img = img
        self.ang = 0
        self.rank = rank
        
        #Setting up the hitbox
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

    def draw(self, gameDisplay):
        if self.img == 0:
            pygame.draw.rect(gameDisplay, (0, 0, 0), (self.x, self.y, self.width, self.height), 0)
        else:
            if self.rank == 2:
                self.ang += 20
                gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(self.img, (self.width+20, self.height+20)), self.ang), (self.x, self.y))
            elif self.rank in [1, 3]:
                gameDisplay.blit(pygame.transform.rotate(pygame.transform.scale(self.img, (self.width+5+((self.rank-1)*5), self.height+10+((self.rank-1)*5))), -1*math.degrees(self.angle)+90), (self.x, self.y))
        #pygame.draw.line(gameDisplay, (0, 0, 0), (self.x, self.y), (self.OldX, self.OldY), 5)

    def movement(self, speed):
        self.x -= self.speed*math.cos(self.angle)*speed
        self.y -= self.speed*math.sin(self.angle)*speed
       

    def update(self, speed, gameDisplay):
        self.draw(gameDisplay)
        self.movement(speed)

        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

class Tower():
    """Class which encapsulates  all towers visuals/mechanics"""
    def __init__(self, x, y, rank):
        self.x, self.y = x, y
        self.width, self.height = 30, 30
        self.rank = rank
        Colors = [(200, 0, 0), (0, 0, 200), (200, 200, 0), (0, 200, 200), (100, 100, 100), (0, 200, 0), (200, 200, 200), (100, 150, 200)]
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
        self.Bombs = []
        self.ExplodeTime = 100
        self.bombRange = 50
        self.Crates = []
        self.crateValue = 25
        self.autoCollect = False
        self.expireTime = 300
        self.glaiveCount = 1
        self.glaiveSpeed = 5
        self.glaiveRings = 1
        self.Glaives = []
    

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

        elif rank == 5:
            #Explosion Factory Tower
            self.descriptions =[[["Fast Production",300],["Faster Production",550],["Damage 4 Days",1000],["Ballistic", 10000]],
                                [["Big Bombs", 175],["Extra Range", 200],["Slow Explode", 800],["Smoke Bomb", 4500]]]
            
            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount  = 1,1,0.5,65,10,0
            self.seeking, self.bulletSpeed, self.camo, self.value, self.fire = False, 10, False, 500, False
            self.lead = False

        elif rank == 6:
            #Money Tower
            self.descriptions =[[["Big Stacks",545],["Bigger Stacks",900],["Money Plantation",2500],["Enterprise", 23500]],
                                [["Long-lasting", 175],["Valued Output", 800],["AutoCollect", 1500],["Fast Money", 4500]]]
            
            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount  = 0,0, 0.1, 100, 0,0
            self.seeking, self.bulletSpeed, self.camo, self.value, self.fire = False, 0, False, 600, False
            self.lead = False

        elif rank == 7:
            self.descriptions =[[["Faster Faster",545],["Double Glaives",900],["QUADRA GLAVES",3500],["Gyro Glaves", 30000]],
                                [["Sonic?", 455],["Damaging Glaves", 800],["Double Ringed Glaives", 1500],["Complete Reform", 50000]]]
            
            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount  = 0,1, 0.1, 100, 0,0
            self.seeking, self.bulletSpeed, self.camo, self.value, self.fire = False, 0, False, 700, False
            self.lead = False

        elif rank == 8:
            self.descriptions =[[["Firen Ma Lazar",1500],["Thick Lazer",2500],["Double Lazer?",50000],["Unbeatable", 100000]],
                                [["Bigger Range", 800],["Biggest Range", 1500],["Mini-Death", 9000],["Unleash Havoc", 26000]]]
            
            self.pierce, self.damage, self.speed, self.range, self.size, self.shotAmount  = 5,1, 3, 200, 10,1
            self.seeking, self.bulletSpeed, self.camo, self.value, self.fire = False, 10, False, 800, False
            self.lead = False

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, (0,150,0), (self.x-5, self.y-5, 40, 40), 0)
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.width, self.height),0)
        
    def attack(self, Monsters, speed, Board, Images, gameDisplay):

        #Display Range of tower:
        #pygame.draw.circle(gameDisplay, (0, 0, 0), (self.x, self.y), self.range, 0)

        #Upgrades set by effects
        effect = [1]
        for affect in self.effects:
            if affect[0] == "Bullet Time":
                effect[0] *= 3
            elif affect[0] == "Forest Fire" and not affect[2]:
                for i in range(36):
                    self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), i*0.2, self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000), self.rank))
                affect[2] = True
            elif affect[0] == "The Arctic":
                for monster in Monsters:
                    monster[0].speedModifier = [0.4, 100]
            elif affect[0] == "Smoke Bomb":
                for monster in Monsters:
                    if monster[0].x >= 0-monster[0].width*1.5:
                        monster[0].confused = True
            elif affect[0] == "Instant Money" and not affect[2]:
                self.cash += 1000
                affect[2] = True
            elif affect[0] == "Complete Reform":
                self.glaiveCount = 10
                self.glaiveRings = 3
                affect[1] = 5
            elif affect[0] == "Unleash Havoc":
                for i in range(36):
                    self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), i*0.2, self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000), self.rank))
                
                
            affect[1] -= 1
            if affect[1] <= 0:
                self.effects.pop(self.effects.index(affect))
                
        img = [Images["Dart"], Images["Shruk"], Images["FireBall"]]    
        #Checking to see if there is a monster in range
        if self.rank in [1,2, 3, 8]  and self.cooldown <= 0:
            for monster in Monsters:
                if math.sqrt((monster[0].x - self.x)**2 + (monster[0].y - self.y)**2) <= self.range and self.cooldown <= 0:
                    if not monster[0].camo or (monster[0].camo and self.camo):

                        angle = math.atan2((self.y-monster[0].y),(self.x-monster[0].x))
                        
                        #print("Self: ", (self.x, self.y), " Monster: ", (monster[0].x, monster[0].y), " ", math.atan2((monster[0].y-self.y),(monster[0].x-self.x)), angle)
                        if self.rank not in [1, 2, 3]:
                            if self.shotAmount == 1:
                                self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), angle, self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000), self.rank))
                            else:
                                for i in range(self.shotAmount):
                                    self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), angle-0.2*(int(self.shotAmount/2)-i), self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000), self.rank))
                        else:
                            if self.shotAmount == 1:
                                self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), angle, self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000), self.rank, img[self.rank-1]))
                            else:
                                for i in range(self.shotAmount):
                                    self.Projectiles.append(Projectile(self.x+int(self.width/2), self.y+int(self.height/2), angle-0.2*(int(self.shotAmount/2)-i), self.pierce, self.size, self.bulletSpeed,random.randint(0,1000000), self.rank, img[self.rank-1]))
                        
                        
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
                        if monster[0].rank > 7 and self.damage != 0:
                            modifier = 1
                        else:
                            modifier = 0
                        monster[0].ReRank(monster[0].rank-self.damage - modifier)
                        if monster[0].rank >= 6 and monster[0].rank - self.damage < 6:
                            monster[0].duplicate = True
                        self.pops += self.damage
                        self.score += self.damage
                        self.cash += self.damage 
            self.cooldown = 50

        Tiles = []
        #Explosion Factory
        if self.rank == 5 and self.cooldown <= 0:
            for j, row in enumerate(Board):
                for i, tile in enumerate(row):
                    if tile == 1 and math.sqrt((i*40 - self.x)**2 + (j*40 - self.y)**2) <= self.range:
                        Tiles.append((i, j))

            if len(Tiles) != 0:
                Pos = Tiles[random.randint(0, len(Tiles)-1)]
                self.Bombs.append(Bomb((self.x+10, self.y+10), (Pos[0]*40+random.randint(0, 20), Pos[1]*40+random.randint(0, 20)), 3, self.ExplodeTime))
            
            self.cooldown = 50

        #Updating all the towers bombs
        for bomb in self.Bombs:
            bomb.update(speed, gameDisplay)
            if bomb.Explosion:
                for monster in Monsters:
                    if math.sqrt((monster[0].x - bomb.x)**2 + (monster[0].y - bomb.y)**2) <= self.bombRange:
                        self.cash += self.damage
                        if monster[0].rank >= 6 and monster[0].rank - self.damage < 6:
                            monster[0].duplicate = True
                        if monster[0].rank > 7 and self.damage != 0:
                            modifier = 1
                        else:
                            modifier = 0
                        if self.damage != 0:
                            monster[0].ReRank(monster[0].rank-self.damage-modifier)
                        self.pops += self.damage
                        self.score += self.damage
                self.Bombs.pop(self.Bombs.index(bomb))

        #Money Tower
        if self.rank == 6 and self.cooldown <= 0:
            if not self.autoCollect:
                run = True
                while run:
                    pos = (self.x+int(self.width/2)+random.randint(-1*self.range, self.range), self.y+int(self.height/2)+random.randint(-1*self.range, self.range))
                    if math.sqrt((pos[0] - self.x)**2 + (pos[1] - self.y)**2) <= self.range:
                        run = False

                self.Crates.append(Crate((self.x+10, self.y+10), (pos[0], pos[1]), self.expireTime, self.crateValue))
            else:
                self.cash += self.crateValue
            self.cooldown = 50

        #Glaive tower
        if self.rank == 7:
            while len(self.Glaives) != self.glaiveCount:
                angle = 0
                if self.glaiveRings == 1:
                    ring = 1
                else:
                    if len(self.Glaives) % 2 == 1:
                        ring = 2
                    else:
                        ring = 1

                if len(self.Glaives) != 0:
                    count = 0
                    currentAngle = 0
                    stop = False
                    for glaive in self.Glaives:
                        if glaive.ring == ring:
                            count += 1
                            if not stop:
                                stop = True
                                currentAngle = glaive.angle
                    if count % 2 == 1:
                        angle = (currentAngle-(6.25/(count+1)))
                    else:
                        angle = (currentAngle-(6.25/(count+1))) - 3.25
         
                self.Glaives.append(Glaive((self.x + int(self.width/4), self.y + int(self.height/4)), angle, ring, self.glaiveSpeed, Images["Glaive"]))

        for glaive in self.Glaives:
            for monster in Monsters:
                if pygame.sprite.collide_rect(glaive, monster[0]) == True and glaive.id not in monster[0].hit and monster[0].rank != 7:
                    monster[0].hit.append(glaive.id)
                    self.cash += self.damage
                    if monster[0].rank >= 6 and monster[0].rank - self.damage < 6:
                        monster[0].duplicate = True
                    if monster[0].rank > 7 and self.damage != 0:
                        modifier = 1
                    else:
                        modifier = 0
                    if self.damage != 0:
                        monster[0].ReRank(monster[0].rank-self.damage+modifier)
                    
                    self.pops += self.damage
                    self.score += self.damage
                        


        #Updating all the towers projectiles
        for projectile in self.Projectiles:
            projectile.update(speed, gameDisplay)
            stop = False
            for monster in Monsters:
                if pygame.sprite.collide_rect(projectile, monster[0]) == True and not stop and projectile.id not in monster[0].hit and ((self.fire and not monster[0].fire[0]) or not self.fire) and (((monster[0].rank == 7) == self.lead) or not monster[0].rank == 7):
                    self.cash += self.damage
                
                    if monster[0].rank >= 6 and monster[0].rank - self.damage < 6:
                        monster[0].duplicate = True
                    if monster[0].rank > 7 and monster[0].rank - self.damage <= 7:
                        modifier = 1
                    else:
                        modifier = 0
                    if self.damage != 0:
                        if monster[0].health - self.damage <= 0:
                            monster[0].ReRank(monster[0].rank-self.damage-modifier)
                        else:
                            monster[0].health -= self.damage
                    
                    monster[0].hit.append(projectile.id)
                    if self.fire:
                        monster[0].fire = [True, self.fireLength, self.fireLength, self.fireLasting, self.fireDamage]
                    stop = True
                    self.pops += self.damage
                    self.score += self.damage
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

    def upgrade(self, cash, gameDisplay):
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

                                elif self.rank == 5:
                                    #Explosion Factory Tower Upgrades
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.speed *= 1.25
                                        elif self.currentUpgrade[i] == 1:
                                            self.speed *= 1.35
                                        elif self.currentUpgrade[i] == 2:
                                            self.damage += 1
                                            self.path = 1
                                        else:
                                            self.speed *= 2
                                            self.damage += 1
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.bombRange *= 1.25
                                        elif self.currentUpgrade[i] == 1:
                                            self.range *= 1.25
                                        elif self.currentUpgrade[i] == 2:
                                            self.ExplodeTime *= 1.5
                                            self.path = 2
                                        else:
                                            self.ability.append(["Smoke Bomb",0,750,200])
                                

                                elif self.rank == 6:
                                    #Money Tower Upgrades
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.speed *= 1.5
                                        elif self.currentUpgrade[i] == 1:
                                            self.speed *= 1.5
                                        elif self.currentUpgrade[i] == 2:
                                            self.speed *= 1.5
                                            self.path = 1
                                        else:
                                            self.speed /= 5
                                            self.crateValue *= 10
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.expireTime *= 2
                                        elif self.currentUpgrade[i] == 1:
                                            self.crateValue *= 2
                                        elif self.currentUpgrade[i] == 2:
                                            self.autoCollect = True
                                            self.path = 2
                                        else:
                                            self.ability.append(["Instant Money",0,750,200])

                                elif self.rank == 7:
                                    #Glaive Tower
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.glaiveSpeed *= 1.5
                                        elif self.currentUpgrade[i] == 1:
                                            self.glaiveCount += 1
                                        elif self.currentUpgrade[i] == 2:
                                            self.glaiveCount += 2
                                            self.path = 1
                                        else:
                                            self.glaiveCount += 4
                                            
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.glaiveSpeed *= 1.4
                                        elif self.currentUpgrade[i] == 1:
                                            self.damage += 1
                                        elif self.currentUpgrade[i] == 2:
                                            self.glaiveRings += 1
                                            self.glaiveCount += 1
                                            self.path = 2
                                        else:
                                            self.ability.append(["Complete Reform",0,-1,200])

                                elif self.rank == 8:
                                    #Glaive Tower
                                    if i == 0:
                                        if self.currentUpgrade[i] == 0:
                                            self.speed *= 5
                                            self.lead = True
                                        elif self.currentUpgrade[i] == 1:
                                            self.size += 10
                                        elif self.currentUpgrade[i] == 2:
                                            self.shotAmount += 1
                                            self.path = 1
                                        else:
                                            self.camo = True
                                            self.shotAmount += 4
                                            
                                        
                                    else:
                                        if self.currentUpgrade[i] == 0:
                                            self.range *= 2
                                        elif self.currentUpgrade[i] == 1:
                                            self.range *= 2
                                        elif self.currentUpgrade[i] == 2:
                                            if self.size == 10:
                                                self.size = 5
                                            else:
                                                self.size = 10
                                            self.path = 2
                                        else:
                                            self.ability.append(["Unleash Havoc",0, 1000,200])
            

                                
                                self.currentUpgrade[i] += 1
                                self.upgrades[i][self.currentUpgrade[i]-1] = 1
                                self.buyCooldown = 50

            self.buyCooldown -= 1
                
    def update(self, Monsters, speed, cash, Board, Images, gameDisplay):
        self.draw(gameDisplay)
        Monsters = self.attack(Monsters, speed, Board, Images, gameDisplay)
        self.upgrade(cash, gameDisplay)

        return Monsters

