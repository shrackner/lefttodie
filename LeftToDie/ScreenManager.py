import pygame
from Animation import Animate, AllSprites
import random
import sys
from soundmanager import soundmanager
import math

class Screen:
    def __init__(self):
        self.go = True
        self.state = "LIFESCREEN"
        self.left = False
        self.screenw = 1024
        self.screenh = 768
        self.sound = soundmanager()
        self.screen = pygame.display.set_mode((self.screenw, self.screenh))
        pygame.font.init()
        self.fontpath = pygame.font.match_font('lucidasans')
        self.font = pygame.font.Font(self.fontpath, 28)
        self.velocity = [.03, 0]
        self.playerpos = [100, 600]

        self.clouds = Clouds()
        self.cloudlist = self.clouds.clouds
        self.cloudsnormal = sorted(self.clouds.cloudimages)
        self.cloudsinverted = sorted(self.clouds.cloudsinverted)
        
        self.backobjects = BackObjects()
        self.startplayer= Animate(AllSprites['playerMoveNormal.png'], 2, 2, 128, 32, 32)
        self.mainplayer= Animate(AllSprites['playerIdleNormal.png'], 2, 2, 500, 32, 32)

        self.current_level = 1
        self.lives = 3
        self.l_screen_clock = pygame.time.Clock()
        self.l_screen_time = 0

        self.jumped = False

    def update(self):
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = True
                    
                elif event.key == pygame.K_RIGHT:
                    self.left = False

        keys = pygame.key.get_pressed()
        #print(keys)
            
        if self.state == "LIFESCREEN":
            self.startplayer.Aupdate()
            self.l_screen_time += self.l_screen_clock.tick()
            if self.l_screen_time >= 3000:
                self.state = "GAMESCREEN"
                self.l_screen_time = 0

        elif self.state == "GAMESCREEN":
            # Right movement
            if keys[pygame.K_RIGHT]:
                self.velocity[0] = 10.0
            
            # Left movement
            elif keys[pygame.K_LEFT]:
                self.velocity[0] = -10.0

            # Jump
            if keys[pygame.K_UP] and not self.jumped:
                self.jumped = True
                self.velocity[1] = -20.0

            if abs(self.velocity[0]) > 10.0:
                if self.velocity[0] > 0:
                    self.velocity[0] = 10.0
                elif self.velocity[0] < 0:
                    self.velocity[0] = -10.0

            self.playerpos[0] += self.velocity[0]
            self.playerpos[1] += self.velocity[1]

            if self.velocity[0] > 0:
                self.velocity[0] -= 1.5
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            elif self.velocity[0] < 0:
                self.velocity[0] += 1.5
                if self.velocity[0] > 0:
                    self.velocity[0] = 0
            else:
                self.velocity[0] = 0
                

            # Gravity application
            self.velocity[1] += 2.5

            if self.playerpos[0] < 0:
                self.playerpos[0] = 0
            elif self.playerpos[0] > 1024:
                self.playerpos[0] = 1024

            if self.playerpos[1] > 600:
                self.jumped = False
                self.playerpos[1] = 600

            print(self.playerpos)
            print()

            self.mainplayer.Aupdate()
            self.clouds.cloudupdate()
            self.backobjects.backupdate(self.left)
                    
        elif self.state == "ENDSCREEN":
            pass

    def draw(self):
        if self.state == "LIFESCREEN":
            background_colour = (0, 0, 0)
            self.screen.fill(background_colour)
            self.startplayer.draw(self.screen, 460, 352)
            text = self.font.render("x " + str(self.lives), True, pygame.Color(255,255,255))
            self.screen.blit(text, (492, 347))
                                              
        elif self.state == "GAMESCREEN":             
            if self.left:
                self.sound.playsound("inverse")
                self.sun = AllSprites["sunInverse.png"]
                self.background = AllSprites["backgroundInverse.png"]
                for i in range(0, len(self.cloudlist)):
                    if "Inverse" not in self.cloudlist[i][3]:
                        self.cloudlist[i][3] = self.cloudsinverted[int(self.cloudlist[i][3][5]) - 1]
                self.bhill = AllSprites["groundBackInverse.png"]
                self.fhill = AllSprites["groundFrontInverse.png"]
                self.fsky = AllSprites["skyFrontInverse.png"]
                self.bsky = AllSprites["skyBackInverse.png"]

                self.bhill2 = AllSprites["groundBackInverse.png"]
                self.fhill2 = AllSprites["groundFrontInverse.png"]
                self.fsky2 = AllSprites["skyFrontInverse.png"]
                self.bsky2 = AllSprites["skyBackInverse.png"]

            else:
                self.sound.playsound("syobon")
                self.sun = AllSprites["sunNormal.png"]
                self.background = AllSprites["backgroundNormal.png"]
                for i in range(0, len(self.cloudlist)):
                    if "Normal" not in self.cloudlist[i][3]:
                        self.cloudlist[i][3] = self.cloudsnormal[int(self.cloudlist[i][3][5]) - 1]

                self.bhill = AllSprites["groundBackNormal.png"]
                self.fhill = AllSprites["groundFrontNormal.png"]
                self.fsky = AllSprites["skyFrontNormal.png"]
                self.bsky = AllSprites["skyBackNormal.png"]

                self.bhill2 = AllSprites["groundBackNormal.png"]
                self.fhill2 = AllSprites["groundFrontNormal.png"]
                self.fsky2 = AllSprites["skyFrontNormal.png"]
                self.bsky2 = AllSprites["skyBackNormal.png"]
                
                self.background = AllSprites["backgroundNormal.png"]

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.sun, (0, 0))
            
            self.screen.blit(self.bsky, (self.backobjects.bskyx,0))
            self.screen.blit(self.bsky2, (self.backobjects.bskyx2,0))
            self.screen.blit(self.bhill, (self.backobjects.bhillx, 534))
            self.screen.blit(self.bhill2, (self.backobjects.bhillx2, 534))

            self.screen.blit(self.fhill, (self.backobjects.fhillx, 593))
            self.screen.blit(self.fhill2, (self.backobjects.fhillx2, 593))
            self.screen.blit(self.fsky, (self.backobjects.fskyx,0))
            self.screen.blit(self.fsky2, (self.backobjects.fskyx2,0))

            for i in range(0, len(self.cloudlist)):
                self.screen.blit(AllSprites[self.cloudlist[i][3]], (self.cloudlist[i][0], self.cloudlist[i][1]))
        
            self.mainplayer.draw(self.screen, self.playerpos[0], self.playerpos[1])

        elif self.state == "ENDSCREEN":
            pass
        
        pygame.display.update()

class BackObjects:
    def __init__(self):
        self.width = 1015
        self.speedf = 10
        self.speedb = 5
        self.min = -self.width
        self.max = self.width
        
        self.fskyx = 0
        self.bskyx = 0
        self.fhillx = 0
        self.bhillx = 0
        
        self.fskyx2 = self.width
        self.bskyx2 = self.width
        self.fhillx2 = self.width
        self.bhillx2 = self.width

    def backupdate(self, inverse):
        if inverse:
            self.fskyx += self.speedf
            self.bskyx += self.speedb
            self.fhillx += self.speedf
            self.bhillx += self.speedb

            if self.fskyx > self.max:
                self.fskyx = self.min

            if self.bskyx > self.max:
                self.bskyx = self.min

            if self.bhillx > self.max:
                self.bhillx = self.min

            if self.fhillx > self.max:
                self.fhillx = self.min
            
            self.fskyx2 += self.speedf
            self.bskyx2 += self.speedb
            self.fhillx2 += self.speedf
            self.bhillx2 += self.speedb

            if self.fskyx2 > self.max:
                self.fskyx2 = self.min

            if self.bskyx2 > self.max:
                self.bskyx2 = self.min

            if self.bhillx2 > self.max:
                self.bhillx2 = self.min

            if self.fhillx2 > self.max:
                self.fhillx2 = self.min

        else:
            self.bskyx -= self.speedb
            self.fskyx -= self.speedf
            self.fhillx -= self.speedf
            self.bhillx -= self.speedb

            if self.fskyx < self.min:
                self.fskyx = self.max

            if self.bskyx < self.min:
                self.bskyx = self.max

            if self.bhillx < self.min:
                self.bhillx = self.max

            if self.fhillx < self.min:
                self.fhillx = self.max
                
            self.fskyx2 -= self.speedf
            self.bskyx2 -= self.speedb
            self.fhillx2 -= self.speedf
            self.bhillx2 -= self.speedb

            if self.fskyx2 < self.min:
                self.fskyx2 = self.max

            if self.bskyx2 < self.min:
                self.bskyx2 = self.max

            if self.bhillx2 < self.min:
                self.bhillx2 = self.max

            if self.fhillx2 < self.min:
                self.fhillx2 = self.max


class Clouds:
    def __init__(self):
        self.cloudnum = random.randint(5,15)

        self.clouds = []
        self.cloudimages = []
        self.cloudsinverted = []
        
        for sprite, image in AllSprites.items():
            if "cloud" in sprite:
                if "Normal" in sprite:
                    self.cloudimages.append(sprite)
                elif "Inverse" in sprite:
                    self.cloudsinverted.append(sprite)

        for i in range(0, self.cloudnum):
            # Random width [0]
            # Random height [1]
            # Random speed [2]
            # Random normal cloud [3]
            self.clouds.append([random.randrange(100, 900),random.randrange(117, 500), random.randint(1,2), self.cloudimages[random.randint(0,len(self.cloudimages) - 1)]])

    def cloudupdate(self):
        for i in range(len(self.clouds)):
            self.clouds[i][0] -= self.clouds[i][2]
            if self.clouds[i][0] + 100 < 0:
                self.clouds[i][0] = 1020
                self.clouds[i][1] = random.randrange(117, 500)
                self.clouds[i][3] = self.cloudimages[random.randint(0, len(self.cloudimages) - 1)]

