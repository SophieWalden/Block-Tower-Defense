import pygame, random, sys, math, os
from pygame.locals import *
 
pygame.init()


class Monster():
    """Class for all the enemies"""
    def __init__(self, rank, wave, camo, Images):

        #Setting up base variables
        self.rank = rank
        self.x, self.y = -100, 200
        self.step = 0
        speed = [2, 3, 4, 5, 6, 4, 3, 1, 2, 3]
        self.speed = speed[self.rank-1] * (1 + (0.01*(int(wave/50)+1)*wave))
        self.wave = wave
        self.height, self.width = 30, 30
        self.dead = False
        Colors = [(200, 0, 0), (0, 0, 200), (0, 200, 0), (255, 255, 0), (255,105,180), (0, 0, 0), (50, 50, 50), (128, 0, 128), (0, 100, 0), (150, 150, 150)]
        self.color = Colors[self.rank-1]
        self.camo = camo
        self.hit = []
        self.fire = [False,0,0,0,0]
        self.speedModifier = [1,0]
        self.permaslow = False
        self.confused = False
        self.health = 1
        if self.rank == 9:
            self.health = 3
        elif self.rank == 10:
            self.health = 50
        self.addMonster = []
        #All checkpoints on the map
        self.checkpoints = [(6, 5), (6, 2), (3, 2), (3, 9), (13, 9), (13, 4), (17, 4)]
        self.duplicate = False
        self.cooldown = 0
        self.img = Images

        #Setting up the hitbox
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.top = self.y
        self.rect.bottom = self.y + self.height
        self.rect.left = self.x
        self.rect.right = self.x + self.width

    def ReRank(self, new_Rank):
        """Changes the rank of the monster to any other rank"""


        if self.rank == 8 and new_Rank != 8:
            self.addMonster.append(5)
        elif self.rank == 10 and new_Rank != 10:
            for i in range(4):
                self.addMonster.append(9)
        if new_Rank <= 0:
            self.dead = True
        else:
            self.rank = new_Rank
            Colors = [(200, 0, 0), (0, 0, 200), (0, 200, 0), (255, 255, 0), (255,105,180), (0, 0, 0), (50, 50, 50), (128, 0, 128), (0, 100, 0), (150, 150, 150)]
            self.color = Colors[self.rank-1]
            speed = [2, 3, 4, 5, 6, 4, 3, 1, 2, 3]
            self.speed = speed[self.rank-1] * (1 + (0.01*(int(self.wave/50)+1)*self.wave))
            if self.rank == 9:
                self.health = 3
            elif self.rank == 10:
                self.health = 50
        
        
    def draw(self, gameDisplay):

 
        if self.rank != 10:    
            pygame.draw.rect(gameDisplay, self.color, (self.x + int(self.width/5), self.y + int(self.height/5), self.width, self.height), 0)
        else:
            pygame.draw.rect(gameDisplay, self.color, (self.x - int(self.width/3), self.y - int(self.height/3), self.width*2, self.height*2), 0)

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

            if self.rank != 10:
                pygame.draw.rect(gameDisplay, (100, 100, 100), (self.x + int(self.width/5), self.y + int(self.height/5), self.width, self.height), 2)
            else:
                pygame.draw.rect(gameDisplay, (100, 100, 100), (self.x - int(self.width/3), self.y - int(self.height/3), self.width*2, self.height*2), 2)

    def movement(self, Lives, speed):

        #Checking to see whether the monster is in range of the next checkpoint
        if not self.confused:
            if (self.checkpoints[self.step][0]*40-self.speed <= self.x <= self.checkpoints[self.step][0]*40+self.speed and
                self.checkpoints[self.step][1]*40-self.speed <= self.y <= self.checkpoints[self.step][1]*40+self.speed):
                self.x, self.y = self.checkpoints[self.step][0]*40, self.checkpoints[self.step][1]*40
                self.step += 1
                if self.step == 7:
                    modifier = 1
                    if self.rank == 10:
                        modifier = 4
                    self.dead = True
                    Lives -= self.rank*modifier
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
        else:
            if self.step == 0:
                xCheck, yCheck = (-10000, 0)
            else:
                xCheck, yCheck = self.checkpoints[self.step-1][0]*40, self.checkpoints[self.step-1][1]*40
            if (xCheck-self.speed <= self.x <= xCheck+self.speed and
                yCheck-self.speed <= self.y <= yCheck+self.speed):
                self.x, self.y = xCheck, yCheck
                self.step -= 1
                if self.step == -1:
                    self.dead = True
                    print("Woah, slow down buddy\nThat's too many Smoke Bombs for 1 man to handle")
            else:
                #Else move it towards it's next checkpoint
                if self.x < xCheck:
                    self.x += int(self.speed*speed*self.speedModifier[0])
                elif self.x > xCheck:
                    self.x -= int(self.speed*speed*self.speedModifier[0])
                elif self.y > yCheck:
                    self.y -= int(self.speed*speed*self.speedModifier[0])
                elif self.y < yCheck:
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

        self.confused = False

        return Lives

    def update(self, Lives, speed, gameDisplay):
        self.draw(gameDisplay)
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
